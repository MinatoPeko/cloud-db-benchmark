#!/usr/bin/env python3
"""
ĐỒ ÁN CHUYÊN NGÀNH KỸ THUẬT PHẦN MỀM - ĐẠI HỌC PHENIKAA
Script kiểm tra trạng thái hoạt động (Healthcheck) của 3 CSDL trong môi trường Dev Container
Vị trí: benchmarks/healthcheck.py
"""

import sys
import time

def check_postgres(host="postgres", port=5432, user="postgres", password="postgres", db="social_benchmark"):
    print("[1/3] Đang kiểm tra kết nối PostgreSQL 16...", end=" ", flush=True)
    try:
        import psycopg2
        start = time.perf_counter()
        conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=db, connect_timeout=5)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        ver = cur.fetchone()[0]
        cur.close()
        conn.close()
        latency = (time.perf_counter() - start) * 1000
        print(f"✅ SẴN SÀNG ({latency:.1f}ms)")
        print(f"      Phiên bản: {ver.split(',')[0]}")
        return True
    except Exception as e:
        # Thử fallback localhost nếu chạy ngoài container
        if host != "localhost":
            return check_postgres(host="localhost", port=port, user=user, password=password, db=db)
        print(f"❌ THẤT BẠI: {e}")
        return False

def check_mongodb(host="mongo", port=27017, db="social_benchmark"):
    print("[2/3] Đang kiểm tra kết nối MongoDB 7.0...", end=" ", flush=True)
    try:
        from pymongo import MongoClient
        start = time.perf_counter()
        client = MongoClient(host=host, port=port, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        build_info = client.admin.command('buildInfo')
        latency = (time.perf_counter() - start) * 1000
        print(f"✅ SẴN SÀNG ({latency:.1f}ms)")
        print(f"      Phiên bản: MongoDB v{build_info.get('version', 'Unknown')}")
        client.close()
        return True
    except Exception as e:
        if host != "localhost":
            return check_mongodb(host="localhost", port=port, db=db)
        print(f"❌ THẤT BẠI: {e}")
        return False

def check_neo4j(uri="bolt://neo4j:7687", user="neo4j", password="password123"):
    print("[3/3] Đang kiểm tra kết nối Neo4j 5.x...", end=" ", flush=True)
    try:
        from neo4j import GraphDatabase
        start = time.perf_counter()
        driver = GraphDatabase.driver(uri, auth=(user, password), connection_timeout=5)
        with driver.session() as session:
            result = session.run("CALL dbms.components() YIELD name, versions RETURN name, versions[0] AS ver")
            record = result.single()
            ver = record["ver"] if record else "5.x"
        driver.close()
        latency = (time.perf_counter() - start) * 1000
        print(f"✅ SẴN SÀNG ({latency:.1f}ms)")
        print(f"      Phiên bản: Neo4j {ver} (Bolt Protocol)")
        return True
    except Exception as e:
        if "localhost" not in uri:
            return check_neo4j(uri="bolt://localhost:7687", user=user, password=password)
        print(f"❌ THẤT BẠI: {e}")
        return False

def main():
    print("=" * 70)
    print("🔍 KIỂM TRA TRẠNG THÁI HỆ SINH THÁI 3 CSDL (DEV CONTAINER HEALTHCHECK)")
    print("=" * 70)
    
    pg_ok = check_postgres()
    mg_ok = check_mongodb()
    n4j_ok = check_neo4j()

    print("-" * 70)
    if pg_ok and mg_ok and n4j_ok:
        print("🎉 TẤT CẢ 3 HỆ QUẢN TRỊ CSDL ĐÃ HOẠT ĐỘNG HOÀN HẢO!")
        print("👉 Bạn đã sẵn sàng để chuyển sang Giai đoạn 4 (Nạp dữ liệu thử nghiệm).")
        print("=" * 70)
        sys.exit(0)
    else:
        print("⚠️ CẢNH BÁO: Có ít nhất một CSDL chưa sẵn sàng. Vui lòng kiểm tra lại dịch vụ.")
        print("=" * 70)
        sys.exit(1)

if __name__ == "__main__":
    main()
