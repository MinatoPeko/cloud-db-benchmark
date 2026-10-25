#!/usr/bin/env python3
"""
data/verify_data.py
Kiểm tra tính toàn vẹn dữ liệu (Data Checksum & Verification) trên cả 3 CSDL:
PostgreSQL, MongoDB, Neo4j.
Sử dụng: python data/verify_data.py
"""

import os
import sys

PG_CONFIG = dict(
    host=os.getenv("PG_HOST", "localhost"),
    port=5432,
    user="postgres",
    password="postgres",
    dbname="social_benchmark",
)
MG_URI = f"mongodb://{os.getenv('MONGO_HOST', 'localhost')}:27017"
N4J_URI = f"bolt://{os.getenv('NEO4J_HOST', 'localhost')}:7687"
N4J_AUTH = ("neo4j", "password123")


def count_postgres():
    import psycopg2

    conn = psycopg2.connect(**PG_CONFIG)
    cur = conn.cursor()
    tables = ["users", "follows", "posts", "comments", "tags", "post_tags"]
    counts = {}
    for tbl in tables:
        cur.execute(f"SELECT COUNT(*) FROM {tbl};")
        counts[tbl] = cur.fetchone()[0]
    cur.close()
    conn.close()
    return counts


def count_mongodb():
    from pymongo import MongoClient

    client = MongoClient(MG_URI, serverSelectionTimeoutMS=5000)
    db = client["social_benchmark"]
    counts = {
        "users": db.users.count_documents({}),
        "follows": db.follows.count_documents({}),
        "posts": db.posts.count_documents({}),
    }
    # Đếm comments trong embedded array
    pipe_comm = [{"$unwind": "$comments"}, {"$count": "total"}]
    res_comm = list(db.posts.aggregate(pipe_comm))
    counts["comments"] = res_comm[0]["total"] if res_comm else 0

    # Đếm unique tags trong posts
    tags = db.posts.distinct("tags")
    counts["tags"] = len(tags)
    client.close()
    return counts


def count_neo4j():
    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(N4J_URI, auth=N4J_AUTH)
    queries = {
        "users": "MATCH (u:User) RETURN count(u)",
        "follows": "MATCH ()-[r:FOLLOWS]->() RETURN count(r)",
        "posts": "MATCH (p:Post) RETURN count(p)",
        "comments": "MATCH (c:Comment) RETURN count(c)",
        "tags": "MATCH (t:Tag) RETURN count(t)",
    }
    counts = {}
    with driver.session() as s:
        for k, q in queries.items():
            counts[k] = s.run(q).single()[0]
    driver.close()
    return counts


def main():
    print("=" * 65)
    print("🔍 KIỂM TRA ĐỐI SOÁT TOÀN VẸN DỮ LIỆU (DATA CHECKSUM VERIFICATION)")
    print("=" * 65)

    counts = {}
    try:
        counts["PostgreSQL"] = count_postgres()
    except Exception as e:
        print(f"⚠️  PostgreSQL: {e}")
        counts["PostgreSQL"] = None

    try:
        counts["MongoDB"] = count_mongodb()
    except Exception as e:
        print(f"⚠️  MongoDB: {e}")
        counts["MongoDB"] = None

    try:
        counts["Neo4j"] = count_neo4j()
    except Exception as e:
        print(f"⚠️  Neo4j: {e}")
        counts["Neo4j"] = None

    entities = ["users", "follows", "posts", "comments", "tags"]
    print(f"\n{'Thực thể':<15} {'PostgreSQL':<15} {'MongoDB':<15} {'Neo4j':<15} {'Khớp 100%'}")
    print("-" * 70)

    all_matched = True
    for ent in entities:
        pg_val = counts["PostgreSQL"].get(ent, "N/A") if counts["PostgreSQL"] else "ERR"
        mg_val = counts["MongoDB"].get(ent, "N/A") if counts["MongoDB"] else "ERR"
        n4_val = counts["Neo4j"].get(ent, "N/A") if counts["Neo4j"] else "ERR"

        matched = (pg_val == mg_val == n4_val) and (pg_val not in ("ERR", "N/A"))
        if not matched:
            all_matched = False
        mark = "✅ Khớp" if matched else "❌ Sai lệch"
        print(f"{ent:<15} {str(pg_val):<15} {str(mg_val):<15} {str(n4_val):<15} {mark}")

    print("-" * 70)
    if all_matched:
        print("🎉 TOÀN BỘ DỮ LIỆU ĐÃ ĐỒNG NHẤT 100% TRÊN CẢ 3 HỆ CSDL!")
    else:
        print("⚠️  Có sự sai lệch hoặc CSDL chưa được nạp/kết nối đầy đủ.")
    print("=" * 70)


if __name__ == "__main__":
    main()
