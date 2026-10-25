#!/usr/bin/env python3
"""
data/import_all.py
Nạp dữ liệu từ data/generated/<scale>/ vào PostgreSQL, MongoDB và Neo4j.
Sử dụng: python data/import_all.py --scale test
"""

import argparse
import csv
import json
import os
import sys
import time

# ── Cấu hình kết nối (fallback localhost khi chạy ngoài container) ────────────
PG_CONFIG = dict(host=os.getenv("PG_HOST", "localhost"), port=5432,
                 user="postgres", password="postgres", dbname="social_benchmark")
MG_URI = f"mongodb://{os.getenv('MONGO_HOST', 'localhost')}:27017"
N4J_URI = f"bolt://{os.getenv('NEO4J_HOST', 'localhost')}:7687"
N4J_AUTH = ("neo4j", "password123")

BATCH = 500   # rows per batch insert

DATA_DIR = os.path.join(os.path.dirname(__file__), "generated")


# ── Helpers ───────────────────────────────────────────────────────────────────
def _csv(path):
    with open(path, encoding="utf-8") as f:
        yield from csv.DictReader(f)

def _batches(iterable, n):
    batch = []
    for row in iterable:
        batch.append(row)
        if len(batch) == n:
            yield batch
            batch = []
    if batch:
        yield batch

def _t(label):
    """Simple timer context: prints elapsed."""
    class _T:
        def __enter__(self):
            self._s = time.perf_counter()
            print(f"  ⏳ {label}...", end=" ", flush=True)
            return self
        def __exit__(self, *_):
            print(f"✅ {time.perf_counter()-self._s:.2f}s")
    return _T()


# ── PostgreSQL ────────────────────────────────────────────────────────────────
def import_postgres(scale_dir: str):
    import psycopg2
    print("\n[PostgreSQL] Đang kết nối...")
    conn = psycopg2.connect(**PG_CONFIG)
    conn.autocommit = False
    cur = conn.cursor()

    schema_sql = os.path.join(os.path.dirname(__file__), "schemas", "postgresql_schema.sql")
    with _t("Áp dụng schema DDL"):
        cur.execute(open(schema_sql, encoding="utf-8").read())
        conn.commit()

    # users
    with _t("Nạp users"):
        for batch in _batches(_csv(f"{scale_dir}/users.csv"), BATCH):
            cur.executemany(
                "INSERT INTO users(id,username,email,full_name,created_at) VALUES(%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
                [(r["id"], r["username"], r["email"], r["full_name"], r["created_at"]) for r in batch]
            )
        conn.commit()

    # tags
    with _t("Nạp tags"):
        for batch in _batches(_csv(f"{scale_dir}/tags.csv"), BATCH):
            cur.executemany(
                "INSERT INTO tags(id,name) VALUES(%s,%s) ON CONFLICT DO NOTHING",
                [(r["id"], r["name"]) for r in batch]
            )
        conn.commit()

    # follows
    with _t("Nạp follows"):
        for batch in _batches(_csv(f"{scale_dir}/follows.csv"), BATCH):
            cur.executemany(
                "INSERT INTO follows(follower_id,followee_id,created_at) VALUES(%s,%s,%s) ON CONFLICT DO NOTHING",
                [(r["follower_id"], r["followee_id"], r["created_at"]) for r in batch]
            )
        conn.commit()

    # posts
    with _t("Nạp posts"):
        for batch in _batches(_csv(f"{scale_dir}/posts.csv"), BATCH):
            cur.executemany(
                "INSERT INTO posts(id,user_id,content,likes_count,created_at) VALUES(%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
                [(r["id"], r["user_id"], r["content"], r["likes_count"], r["created_at"]) for r in batch]
            )
        conn.commit()

    # comments
    with _t("Nạp comments"):
        for batch in _batches(_csv(f"{scale_dir}/comments.csv"), BATCH):
            cur.executemany(
                "INSERT INTO comments(id,post_id,user_id,content,created_at) VALUES(%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
                [(r["id"], r["post_id"], r["user_id"], r["content"], r["created_at"]) for r in batch]
            )
        conn.commit()

    # post_tags
    with _t("Nạp post_tags"):
        for batch in _batches(_csv(f"{scale_dir}/post_tags.csv"), BATCH):
            cur.executemany(
                "INSERT INTO post_tags(post_id,tag_id) VALUES(%s,%s) ON CONFLICT DO NOTHING",
                [(r["post_id"], r["tag_id"]) for r in batch]
            )
        conn.commit()

    cur.close(); conn.close()
    print("  ✅ PostgreSQL hoàn tất.")


# ── MongoDB ───────────────────────────────────────────────────────────────────
def import_mongodb(scale_dir: str):
    from pymongo import MongoClient, ASCENDING, DESCENDING
    from pymongo.errors import BulkWriteError
    print("\n[MongoDB] Đang kết nối...")
    client = MongoClient(MG_URI, serverSelectionTimeoutMS=5000)
    db = client["social_benchmark"]

    # Drop & recreate (schema validator từ mongodb_schema.js đã được áp ở healthcheck/setup)
    # Ở đây ta chỉ đảm bảo collections tồn tại và đã index
    for col in ("users", "follows", "posts"):
        db[col].drop()

    # Indexes
    db.users.create_index([("username", ASCENDING)], unique=True)
    db.users.create_index([("email", ASCENDING)], unique=True)
    db.follows.create_index([("follower_id", ASCENDING), ("followee_id", ASCENDING)], unique=True)
    db.follows.create_index([("followee_id", ASCENDING)])
    db.posts.create_index([("user_id", ASCENDING), ("created_at", DESCENDING)])
    db.posts.create_index([("tags", ASCENDING)])
    db.posts.create_index([("comments.user_id", ASCENDING)])

    def _safe_insert(col, docs):
        try:
            col.insert_many(docs, ordered=False)
        except BulkWriteError:
            pass  # duplicate key — bỏ qua

    # users
    with _t("Nạp users"):
        for batch in _batches(_csv(f"{scale_dir}/users.csv"), BATCH):
            _safe_insert(db.users, [
                {"_id": int(r["id"]), "username": r["username"], "email": r["email"],
                 "full_name": r["full_name"], "created_at": r["created_at"]}
                for r in batch
            ])

    # follows
    with _t("Nạp follows"):
        for batch in _batches(_csv(f"{scale_dir}/follows.csv"), BATCH):
            _safe_insert(db.follows, [
                {"follower_id": int(r["follower_id"]), "followee_id": int(r["followee_id"]),
                 "created_at": r["created_at"]}
                for r in batch
            ])

    # posts (từ mongo_posts.jsonl — đã có embedded comments và tags)
    with _t("Nạp posts (JSONL)"):
        with open(f"{scale_dir}/mongo_posts.jsonl", encoding="utf-8") as f:
            for batch in _batches(f, BATCH):
                _safe_insert(db.posts, [json.loads(line) for line in batch])

    client.close()
    print("  ✅ MongoDB hoàn tất.")


# ── Neo4j ─────────────────────────────────────────────────────────────────────
def import_neo4j(scale_dir: str):
    from neo4j import GraphDatabase
    print("\n[Neo4j] Đang kết nối...")
    driver = GraphDatabase.driver(N4J_URI, auth=N4J_AUTH)

    schema_cypher = os.path.join(os.path.dirname(__file__), "schemas", "neo4j_schema.cypher")
    with driver.session() as s:
        # Áp constraints & indexes từ schema file (bỏ qua comment lines)
        with _t("Áp dụng schema Cypher"):
            for stmt in open(schema_cypher, encoding="utf-8").read().split(";"):
                stmt = stmt.strip()
                if stmt and not stmt.startswith("//"):
                    try:
                        s.run(stmt)
                    except Exception:
                        pass  # IF NOT EXISTS — an toàn khi chạy lại

        # Xóa dữ liệu cũ
        with _t("Xóa dữ liệu cũ"):
            s.run("MATCH (n) DETACH DELETE n")

    # users → (:User) nodes
    with _t("Nạp User nodes"):
        with driver.session() as s:
            for batch in _batches(_csv(f"{scale_dir}/users.csv"), BATCH):
                s.run(
                    "UNWIND $rows AS r "
                    "MERGE (u:User {id: toInteger(r.id)}) "
                    "SET u.username=r.username, u.email=r.email, "
                    "    u.full_name=r.full_name, u.created_at=r.created_at",
                    rows=batch
                )

    # tags → (:Tag) nodes
    with _t("Nạp Tag nodes"):
        with driver.session() as s:
            for batch in _batches(_csv(f"{scale_dir}/tags.csv"), BATCH):
                s.run(
                    "UNWIND $rows AS r MERGE (t:Tag {name: r.name})",
                    rows=batch
                )

    # follows → [:FOLLOWS] relationships
    with _t("Nạp FOLLOWS relationships"):
        with driver.session() as s:
            for batch in _batches(_csv(f"{scale_dir}/follows.csv"), BATCH):
                s.run(
                    "UNWIND $rows AS r "
                    "MATCH (a:User {id: toInteger(r.follower_id)}), (b:User {id: toInteger(r.followee_id)}) "
                    "MERGE (a)-[:FOLLOWS {created_at: r.created_at}]->(b)",
                    rows=batch
                )

    # posts → (:Post) + [:AUTHORED]
    with _t("Nạp Post nodes + AUTHORED"):
        with driver.session() as s:
            for batch in _batches(_csv(f"{scale_dir}/posts.csv"), BATCH):
                s.run(
                    "UNWIND $rows AS r "
                    "MERGE (p:Post {id: toInteger(r.id)}) "
                    "SET p.content=r.content, p.likes_count=toInteger(r.likes_count), p.created_at=r.created_at "
                    "WITH p, r "
                    "MATCH (u:User {id: toInteger(r.user_id)}) "
                    "MERGE (u)-[:AUTHORED]->(p)",
                    rows=batch
                )

    # post_tags → [:TAGGED_WITH] (cần tag_name vì Tag node dùng name làm key)
    with _t("Nạp TAGGED_WITH relationships"):
        tag_map = {r["id"]: r["name"] for r in _csv(f"{scale_dir}/tags.csv")}
        with driver.session() as s:
            for batch in _batches(_csv(f"{scale_dir}/post_tags.csv"), BATCH):
                rows_with_name = [{"post_id": r["post_id"], "tag_name": tag_map[r["tag_id"]]} for r in batch]
                s.run(
                    "UNWIND $rows AS r "
                    "MATCH (p:Post {id: toInteger(r.post_id)}), (t:Tag {name: r.tag_name}) "
                    "MERGE (p)-[:TAGGED_WITH]->(t)",
                    rows=rows_with_name
                )

    # Comments → (:Comment) + [:WROTE] + [:ON_POST]
    with _t("Nạp Comment nodes + WROTE + ON_POST"):
        with driver.session() as s:
            for batch in _batches(_csv(f"{scale_dir}/comments.csv"), BATCH):
                s.run(
                    "UNWIND $rows AS r "
                    "MERGE (c:Comment {id: toInteger(r.id)}) "
                    "SET c.content=r.content, c.created_at=r.created_at "
                    "WITH c, r "
                    "MATCH (u:User {id: toInteger(r.user_id)}), (p:Post {id: toInteger(r.post_id)}) "
                    "MERGE (u)-[:WROTE]->(c) "
                    "MERGE (c)-[:ON_POST]->(p)",
                    rows=batch
                )

    driver.close()
    print("  ✅ Neo4j hoàn tất.")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Nạp dữ liệu vào 3 CSDL.")
    parser.add_argument("--scale", default="test",
                        choices=["test", "small", "medium", "large"],
                        help="Quy mô dữ liệu (phải đã sinh bằng datagen.py)")
    parser.add_argument("--db", default="all",
                        choices=["all", "postgres", "mongodb", "neo4j"],
                        help="Chọn CSDL cần nạp")
    args = parser.parse_args()

    scale_dir = os.path.join(DATA_DIR, args.scale)
    if not os.path.isdir(scale_dir):
        sys.exit(f"❌ Không tìm thấy thư mục: {scale_dir}. Hãy chạy datagen.py --scale {args.scale} trước.")

    print(f"\n{'='*60}")
    print(f"📥 IMPORT DỮ LIỆU QUY MÔ [{args.scale.upper()}] → {args.db.upper()}")
    print(f"{'='*60}")
    t0 = time.perf_counter()

    run_pg  = args.db in ("all", "postgres")
    run_mg  = args.db in ("all", "mongodb")
    run_n4j = args.db in ("all", "neo4j")

    if run_pg:
        try:
            import_postgres(scale_dir)
        except Exception as e:
            print(f"  ❌ PostgreSQL thất bại: {e}")

    if run_mg:
        try:
            import_mongodb(scale_dir)
        except Exception as e:
            print(f"  ❌ MongoDB thất bại: {e}")

    if run_n4j:
        try:
            import_neo4j(scale_dir)
        except Exception as e:
            print(f"  ❌ Neo4j thất bại: {e}")

    print(f"\n🎉 Hoàn tất import trong {time.perf_counter()-t0:.2f}s\n")


if __name__ == "__main__":
    main()
