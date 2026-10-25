#!/usr/bin/env python3
"""
benchmarks/runner.py
Benchmark engine: thực thi 7 Use Case trên 3 CSDL, đo Latency + QPS + tài nguyên.
Kết quả ghi vào results/data/results_<scale>_<timestamp>.csv

Sử dụng:
    python benchmarks/runner.py --scale test
    python benchmarks/runner.py --scale small --workers 10 --rounds 30
    python benchmarks/runner.py --all --scale small
"""

import argparse
import csv
import os
import random
import statistics
import sys
import time
from datetime import datetime

try:
    from benchmarks.monitor import ResourceMonitor
except ModuleNotFoundError:
    from monitor import ResourceMonitor

# ── Connection helpers (lazy import để tránh crash khi DB không có mặt) ────────
PG_CONFIG = dict(host=os.getenv("PG_HOST", "localhost"), port=5432,
                 user="postgres", password="postgres", dbname="social_benchmark")
MG_URI    = f"mongodb://{os.getenv('MONGO_HOST', 'localhost')}:27017"
N4J_URI   = f"bolt://{os.getenv('NEO4J_HOST', 'localhost')}:7687"
N4J_AUTH  = ("neo4j", "password123")

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results", "data")


# ── Benchmark definitions ──────────────────────────────────────────────────────
# Mỗi entry: (uc_id, uc_name, db_name, callable(conn, params) -> None)

def _pg_benchmarks(conn):
    """Trả về list (uc_id, name, fn) cho PostgreSQL."""
    import psycopg2

    def run(sql, params=()):
        cur = conn.cursor()
        cur.execute(sql, params)
        cur.fetchall()
        cur.close()

    return [
        ("UC-01", "Single Insert",
         lambda p: run("INSERT INTO users(id,username,email,full_name,created_at) "
                       "VALUES(%s,%s,%s,%s,NOW()) ON CONFLICT DO NOTHING",
                       (p["uid_new"], p["username_new"], p["email_new"], "Bench User"))),
        ("UC-02", "Point Read",
         lambda p: run("SELECT * FROM users WHERE id=%s", (p["uid"],))),
        ("UC-03", "Join Read",
         lambda p: run("SELECT p.*,c.* FROM posts p LEFT JOIN comments c ON c.post_id=p.id WHERE p.id=%s", (p["pid"],))),
        ("UC-04", "Aggregation",
         lambda p: run("SELECT t.name,COUNT(pt.post_id) FROM tags t JOIN post_tags pt ON pt.tag_id=t.id GROUP BY t.name ORDER BY 2 DESC")),
        ("UC-05", "1-hop Traversal",
         lambda p: run("SELECT followee_id FROM follows WHERE follower_id=%s", (p["uid"],))),
        ("UC-06", "2-hop FOAF",
         lambda p: run(
             "SELECT f2.followee_id,COUNT(*) AS mc FROM follows f1 "
             "JOIN follows f2 ON f2.follower_id=f1.followee_id "
             "WHERE f1.follower_id=%s AND f2.followee_id<>%s "
             "AND f2.followee_id NOT IN(SELECT followee_id FROM follows WHERE follower_id=%s) "
             "GROUP BY f2.followee_id ORDER BY mc DESC LIMIT 10",
             (p["uid"], p["uid"], p["uid"]))),
        ("UC-07", "Shortest Path",
         lambda p: run(
             "WITH RECURSIVE path_cte AS ("
             "  SELECT follower_id,followee_id,1 AS depth,ARRAY[follower_id] AS visited FROM follows WHERE follower_id=%s"
             "  UNION ALL"
             "  SELECT pc.follower_id,f.followee_id,pc.depth+1,pc.visited||f.followee_id"
             "  FROM path_cte pc JOIN follows f ON f.follower_id=pc.followee_id"
             "  WHERE pc.depth<4 AND NOT(f.followee_id=ANY(pc.visited))"
             ") SELECT visited||ARRAY[followee_id],depth FROM path_cte WHERE followee_id=%s ORDER BY depth LIMIT 1",
             (p["src"], p["dst"]))),
    ]


def _mg_benchmarks(db):
    """Trả về list (uc_id, name, fn) cho MongoDB."""
    from bson import Int64

    return [
        ("UC-01", "Single Insert",
         lambda p: db.users.insert_one(
             {"_id": p["uid_new"], "username": p["username_new"], "email": p["email_new"],
              "full_name": "Bench User", "created_at": datetime.utcnow()}).acknowledged),
        ("UC-02", "Point Read",
         lambda p: db.users.find_one({"_id": p["uid"]})),
        ("UC-03", "Embedded Read",
         lambda p: db.posts.find_one({"_id": p["pid"]})),
        ("UC-04", "Aggregation",
         lambda p: list(db.posts.aggregate([
             {"$unwind": "$tags"},
             {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
             {"$sort": {"count": -1}}
         ]))),
        ("UC-05", "1-hop Traversal",
         lambda p: list(db.follows.find({"follower_id": p["uid"]}, {"followee_id": 1, "_id": 0}))),
        ("UC-06", "2-hop FOAF",
         lambda p: list(db.follows.aggregate([
             {"$match": {"follower_id": p["uid"]}},
             {"$graphLookup": {"from": "follows", "startWith": "$followee_id",
                               "connectFromField": "followee_id", "connectToField": "follower_id",
                               "as": "foaf", "maxDepth": 1}},
             {"$unwind": "$foaf"},
             {"$group": {"_id": "$foaf.followee_id", "mc": {"$sum": 1}}},
             {"$sort": {"mc": -1}}, {"$limit": 10}
         ]))),
        ("UC-07", "Shortest Path (graphLookup)",
         lambda p: list(db.follows.aggregate([
             {"$match": {"follower_id": p["src"]}},
             {"$graphLookup": {"from": "follows", "startWith": "$followee_id",
                               "connectFromField": "followee_id", "connectToField": "follower_id",
                               "as": "path", "maxDepth": 3, "depthField": "depth"}},
             {"$unwind": "$path"},
             {"$match": {"path.followee_id": p["dst"]}},
             {"$sort": {"path.depth": 1}}, {"$limit": 1}
         ]))),
    ]


def _n4j_benchmarks(driver):
    """Trả về list (uc_id, name, fn) cho Neo4j."""

    def run(cypher, **kw):
        with driver.session() as s:
            return s.run(cypher, **kw).data()

    return [
        ("UC-01", "Single Insert",
         lambda p: run("MERGE (u:User {id: $uid}) SET u.username=$un, u.email=$em, u.full_name='Bench User'",
                       uid=p["uid_new"], un=p["username_new"], em=p["email_new"])),
        ("UC-02", "Point Read",
         lambda p: run("MATCH (u:User {id: $uid}) RETURN u", uid=p["uid"])),
        ("UC-03", "Join Read",
         lambda p: run("MATCH (p:Post {id: $pid}) OPTIONAL MATCH (c:Comment)-[:ON_POST]->(p) RETURN p, collect(c) AS comments",
                       pid=p["pid"])),
        ("UC-04", "Aggregation",
         lambda p: run("MATCH (t:Tag)<-[:TAGGED_WITH]-(p:Post) RETURN t.name AS tag, count(p) AS cnt ORDER BY cnt DESC")),
        ("UC-05", "1-hop Traversal",
         lambda p: run("MATCH (u:User {id: $uid})-[:FOLLOWS]->(f:User) RETURN f.id", uid=p["uid"])),
        ("UC-06", "2-hop FOAF",
         lambda p: run(
             "MATCH (u:User {id: $uid})-[:FOLLOWS]->()-[:FOLLOWS]->(foaf:User) "
             "WHERE NOT (u)-[:FOLLOWS]->(foaf) AND u<>foaf "
             "RETURN foaf.id, count(*) AS mc ORDER BY mc DESC LIMIT 10", uid=p["uid"])),
        ("UC-07", "Shortest Path",
         lambda p: run(
             "MATCH path=shortestPath((src:User {id:$src})-[:FOLLOWS*..4]->(dst:User {id:$dst})) "
             "RETURN [n IN nodes(path)|n.id] AS path, length(path) AS hops",
             src=p["src"], dst=p["dst"])),
    ]


# ── Core timing logic ──────────────────────────────────────────────────────────
def _measure(fn, params, rounds: int) -> dict:
    """Chạy fn(params) nhiều lần, trả về dict latency thống kê (ms)."""
    latencies = []
    for _ in range(rounds):
        t0 = time.perf_counter()
        try:
            fn(params)
        except Exception:
            pass
        latencies.append((time.perf_counter() - t0) * 1000)

    latencies.sort()
    n = len(latencies)
    return {
        "mean_ms":  round(statistics.mean(latencies), 3),
        "p50_ms":   round(latencies[int(n * 0.50)], 3),
        "p95_ms":   round(latencies[int(n * 0.95)], 3),
        "p99_ms":   round(latencies[int(n * 0.99)], 3),
        "min_ms":   round(latencies[0], 3),
        "max_ms":   round(latencies[-1], 3),
        "qps":      round(n / (sum(latencies) / 1000), 1) if sum(latencies) > 0 else 0,
        "rounds":   n,
    }


def _sample_params(scale_dir: str, extra_offset: int = 999_000) -> dict:
    """Đọc một vài ID ngẫu nhiên từ users/posts CSV làm tham số benchmark."""
    import csv as _csv_mod
    users_path = os.path.join(scale_dir, "users.csv")
    posts_path = os.path.join(scale_dir, "posts.csv")

    user_ids, post_ids = [], []
    with open(users_path, encoding="utf-8") as f:
        for row in _csv_mod.DictReader(f):
            user_ids.append(int(row["id"]))
    with open(posts_path, encoding="utf-8") as f:
        for row in _csv_mod.DictReader(f):
            post_ids.append(int(row["id"]))

    uid  = random.choice(user_ids)
    uid2 = random.choice([x for x in user_ids if x != uid])
    pid  = random.choice(post_ids)
    new_id = max(user_ids) + extra_offset + random.randint(1, 10000)

    return {
        "uid": uid, "src": uid, "dst": uid2, "pid": pid,
        "uid_new": new_id,
        "username_new": f"bench_{new_id}",
        "email_new": f"bench_{new_id}@bench.test",
    }


# ── Per-DB runners ─────────────────────────────────────────────────────────────
def run_postgres(scale_dir, rounds, results):
    import psycopg2
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        conn.autocommit = True
        params = _sample_params(scale_dir)
        benchmarks = _pg_benchmarks(conn)
        for uc_id, uc_name, fn in benchmarks:
            monitor = ResourceMonitor().start()
            stats = _measure(fn, params, rounds)
            res = monitor.stop()
            results.append({"db": "PostgreSQL", "uc_id": uc_id, "uc_name": uc_name, **stats, **res})
            print(f"  [{uc_id}] {uc_name}: mean={stats['mean_ms']}ms  p99={stats['p99_ms']}ms  qps={stats['qps']}")
        conn.close()
    except Exception as e:
        print(f"  ❌ PostgreSQL error: {e}")


def run_mongodb(scale_dir, rounds, results):
    from pymongo import MongoClient
    try:
        client = MongoClient(MG_URI, serverSelectionTimeoutMS=5000)
        db = client["social_benchmark"]
        params = _sample_params(scale_dir)
        benchmarks = _mg_benchmarks(db)
        for uc_id, uc_name, fn in benchmarks:
            monitor = ResourceMonitor().start()
            stats = _measure(fn, params, rounds)
            res = monitor.stop()
            results.append({"db": "MongoDB", "uc_id": uc_id, "uc_name": uc_name, **stats, **res})
            print(f"  [{uc_id}] {uc_name}: mean={stats['mean_ms']}ms  p99={stats['p99_ms']}ms  qps={stats['qps']}")
        client.close()
    except Exception as e:
        print(f"  ❌ MongoDB error: {e}")


def run_neo4j(scale_dir, rounds, results):
    from neo4j import GraphDatabase
    try:
        driver = GraphDatabase.driver(N4J_URI, auth=N4J_AUTH)
        params = _sample_params(scale_dir)
        benchmarks = _n4j_benchmarks(driver)
        for uc_id, uc_name, fn in benchmarks:
            monitor = ResourceMonitor().start()
            stats = _measure(fn, params, rounds)
            res = monitor.stop()
            results.append({"db": "Neo4j", "uc_id": uc_id, "uc_name": uc_name, **stats, **res})
            print(f"  [{uc_id}] {uc_name}: mean={stats['mean_ms']}ms  p99={stats['p99_ms']}ms  qps={stats['qps']}")
        driver.close()
    except Exception as e:
        print(f"  ❌ Neo4j error: {e}")


def save_results(results: list[dict], scale: str):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(RESULTS_DIR, f"results_{scale}_{ts}.csv")
    if not results:
        print("⚠️  Không có kết quả để lưu.")
        return path
    fieldnames = list(results[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(results)
    print(f"\n💾 Kết quả đã lưu: {path}")
    return path


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Benchmark engine cho 3 CSDL.")
    parser.add_argument("--scale",   default="test", choices=["test", "small", "medium", "large"])
    parser.add_argument("--rounds", "--iterations", dest="rounds", type=int, default=20, help="Số vòng lặp mỗi use case (mặc định: 20)")
    parser.add_argument("--db",      default="all", choices=["all", "postgres", "mongodb", "neo4j"])
    parser.add_argument("--all",     action="store_true", help="Tương đương --db all")
    args = parser.parse_args()

    if args.all:
        args.db = "all"

    data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "generated", args.scale)
    if not os.path.isdir(data_dir):
        sys.exit(f"❌ Không tìm thấy {data_dir}. Chạy datagen.py trước.")

    print(f"\n{'='*65}")
    print(f"⚡ BENCHMARK ENGINE  |  Scale={args.scale.upper()}  |  Rounds={args.rounds}")
    print(f"{'='*65}")

    results = []

    if args.db in ("all", "postgres"):
        print("\n🐘 PostgreSQL:")
        run_postgres(data_dir, args.rounds, results)

    if args.db in ("all", "mongodb"):
        print("\n🍃 MongoDB:")
        run_mongodb(data_dir, args.rounds, results)

    if args.db in ("all", "neo4j"):
        print("\n🔵 Neo4j:")
        run_neo4j(data_dir, args.rounds, results)

    save_results(results, args.scale)

    # In bảng tóm tắt
    print(f"\n{'─'*65}")
    print(f"{'DB':<12} {'UC':<8} {'Name':<22} {'mean ms':>8} {'p99 ms':>8} {'QPS':>7}")
    print(f"{'─'*65}")
    for r in results:
        print(f"{r['db']:<12} {r['uc_id']:<8} {r['uc_name']:<22} {r['mean_ms']:>8} {r['p99_ms']:>8} {r['qps']:>7}")
    print(f"{'─'*65}\n")


if __name__ == "__main__":
    # Cho phép chạy trực tiếp: python benchmarks/runner.py
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    main()
