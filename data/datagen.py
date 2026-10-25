#!/usr/bin/env python3
"""
============================================================================
ĐỒ ÁN CHUYÊN NGÀNH KỸ THUẬT PHẦN MỀM - ĐẠI HỌC PHENIKAA
Bộ sinh dữ liệu ngẫu nhiên thực tế (Realistic Synthetic Data Generator)
Mô hình Mạng xã hội (Social Network: Users, Follows, Posts, Comments, Tags)
Vị trí: data/datagen.py
============================================================================
"""

import argparse
import csv
import json
import os
import random
import time
from datetime import datetime, timedelta

# ============================================================================
# CẤU HÌNH QUY MÔ DỮ LIỆU (DATA SCALING TIERS)
# ============================================================================
SCALE_CONFIGS = {
    "test": {
        "num_users": 100,
        "avg_follows_per_user": 5,
        "avg_posts_per_user": 2,
        "avg_comments_per_post": 2,
    },
    "small": {
        "num_users": 10_000,
        "avg_follows_per_user": 5,
        "avg_posts_per_user": 3,
        "avg_comments_per_post": 3,
    },
    "medium": {
        "num_users": 100_000,
        "avg_follows_per_user": 5,
        "avg_posts_per_user": 3,
        "avg_comments_per_post": 3,
    },
    "large": {
        "num_users": 500_000,
        "avg_follows_per_user": 5,
        "avg_posts_per_user": 3,
        "avg_comments_per_post": 3,
    },
}

# Danh sách mẫu phục vụ sinh dữ liệu nhanh và chuẩn xác
FIRST_NAMES = [
    "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng",
    "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Alex", "David", "Emma", "John"
]
MIDDLE_NAMES = ["Văn", "Thị", "Đức", "Thành", "Minh", "Thanh", "Hải", "Quang", "Anh", "Hoàng"]
LAST_NAMES = [
    "Hùng", "Cường", "Dũng", "Nam", "Long", "Tuấn", "Hương", "Lan", "Trang", "Mai",
    "Tú", "Bình", "Sơn", "Linh", "Thảo", "Hà", "Phong", "Phúc", "Khang", "Tâm"
]
TAG_POOL = [
    "technology", "database", "sql", "nosql", "graphdb", "cloud", "codespaces",
    "postgresql", "mongodb", "neo4j", "python", "docker", "devops", "bigdata",
    "ai", "machinelearning", "deeplearning", "dataengineering", "backend",
    "distributed", "benchmark", "softwareengineering", "phenikaa", "research",
    "performance", "webdevelopment", "algorithms", "datascience", "linux", "git"
]
POST_TEMPLATES = [
    "Đang nghiên cứu và thử nghiệm hiệu năng của {tag} trên môi trường cloud.",
    "Hôm nay tối ưu hóa thành công cấu hình bộ nhớ cho {tag}, kết quả rất ấn tượng!",
    "Chia sẻ tài liệu hay về kiến trúc lưu trữ và đánh chỉ mục trong {tag}.",
    "So sánh tốc độ xử lý truy vấn quan hệ đa tầng giữa SQL và Graph DB.",
    "Benchmark kết quả đo độ trễ và thông lượng khi nạp dữ liệu lớn vào {tag}.",
    "Kinh nghiệm debug và giám sát tài nguyên CPU, RAM trên GitHub Codespaces.",
    "Tổng kết tiến độ đồ án tốt nghiệp tuần này: Đã hoàn thiện schema và data pipeline."
]
COMMENT_TEMPLATES = [
    "Bài viết rất hữu ích, cảm ơn tác giả đã chia sẻ!",
    "Bạn có thể chia sẻ thêm về thông số đo độ trễ p99 không?",
    "Mình cũng đang thử nghiệm giải pháp này, thấy hiệu năng rất ổn định.",
    "Đồng ý với quan điểm so sánh này, kiến trúc đồ thị thực sự vượt trội ở kịch bản FOAF.",
    "Rất ấn tượng với kết quả benchmark trên hạ tầng cloud!",
    "Cho mình hỏi phiên bản database bạn đang sử dụng là bản mấy vậy?"
]


def generate_preferential_attachment_follows(num_users: int, avg_edges: int) -> list[tuple[int, int, str]]:
    """
    Sinh mạng lưới quan hệ Follows theo quy luật Barabási-Albert (Power-Law).
    Mô phỏng mạng xã hội thực tế: một số 'KOL/Influencer' có rất nhiều người theo dõi,
    đa số người dùng bình thường có ít người theo dõi.
    """
    m = max(1, avg_edges)
    edges = set()
    node_degrees = []

    # Khởi tạo cụm ban đầu với m + 1 đỉnh liên kết lẫn nhau
    initial_nodes = min(num_users, m + 1)
    for i in range(1, initial_nodes + 1):
        for j in range(1, initial_nodes + 1):
            if i != j:
                edges.add((i, j))
                node_degrees.extend([i, j])

    base_time = datetime(2026, 1, 1, 0, 0, 0)
    
    # Sinh liên kết ưu tiên (Preferential Attachment)
    for new_node in range(initial_nodes + 1, num_users + 1):
        # Chọn ngẫu nhiên m mục tiêu dựa trên bậc phân phối (degree)
        targets = set()
        attempts = 0
        while len(targets) < m and attempts < m * 5:
            target = random.choice(node_degrees)
            if target != new_node and (new_node, target) not in edges:
                targets.add(target)
            attempts += 1

        for target in targets:
            edges.add((new_node, target))
            node_degrees.extend([new_node, target])

    # Chuyển đổi thành danh sách tuple kèm thời gian tạo
    result = []
    total_edges = len(edges)
    for follower, followee in edges:
        rand_seconds = random.randint(0, 90 * 86400)
        created_at = (base_time + timedelta(seconds=rand_seconds)).isoformat() + "Z"
        result.append((follower, followee, created_at))

    return result


def generate_dataset(scale: str, output_dir: str):
    """
    Sinh trọn bộ dữ liệu Mạng xã hội và xuất ra các file CSV và JSON Lines.
    """
    config = SCALE_CONFIGS.get(scale)
    if not config:
        raise ValueError(f"Quy mô '{scale}' không hợp lệ. Chọn một trong: {list(SCALE_CONFIGS.keys())}")

    target_dir = os.path.join(output_dir, scale)
    os.makedirs(target_dir, exist_ok=True)

    print(f"\n========================================================")
    print(f"🚀 BẮT ĐẦU SINH DỮ LIỆU QUY MÔ: [{scale.upper()}]")
    print(f"📁 Thư mục xuất: {target_dir}")
    print(f"========================================================")
    start_total_time = time.time()

    base_time = datetime(2026, 1, 1, 0, 0, 0)
    num_users = config["num_users"]

    # ------------------------------------------------------------------------
    # 1. SINH DỮ LIỆU USERS
    # ------------------------------------------------------------------------
    print(f"⏳ [1/5] Đang sinh {num_users:,} người dùng (Users)...")
    t0 = time.time()
    users = []
    users_csv_path = os.path.join(target_dir, "users.csv")

    with open(users_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "username", "email", "full_name", "created_at"])
        for uid in range(1, num_users + 1):
            full_name = f"{random.choice(FIRST_NAMES)} {random.choice(MIDDLE_NAMES)} {random.choice(LAST_NAMES)}"
            username = f"user_{uid}"
            email = f"user_{uid}@benchmark.phenikaa-uni.edu.vn"
            created_at = (base_time + timedelta(seconds=random.randint(0, 30 * 86400))).isoformat() + "Z"
            users.append({"id": uid, "username": username, "email": email, "full_name": full_name, "created_at": created_at})
            writer.writerow([uid, username, email, full_name, created_at])

    print(f"✅ Hoàn thành Users trong {time.time() - t0:.2f}s -> {users_csv_path}")

    # ------------------------------------------------------------------------
    # 2. SINH DỮ LIỆU TAGS
    # ------------------------------------------------------------------------
    print(f"⏳ [2/5] Đang sinh danh mục {len(TAG_POOL)} Thẻ chủ đề (Tags)...")
    tags_csv_path = os.path.join(target_dir, "tags.csv")
    tags_list = []
    with open(tags_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name"])
        for idx, tag_name in enumerate(TAG_POOL, start=1):
            tags_list.append({"id": idx, "name": tag_name})
            writer.writerow([idx, tag_name])

    print(f"✅ Hoàn thành Tags -> {tags_csv_path}")

    # ------------------------------------------------------------------------
    # 3. SINH DỮ LIỆU FOLLOWS (ĐỒ THỊ CÓ HƯỚNG THEO LUẬT BARABÁSI-ALBERT)
    # ------------------------------------------------------------------------
    print(f"⏳ [3/5] Đang sinh quan hệ Theo dõi (Follows Graph)...")
    t0 = time.time()
    follows = generate_preferential_attachment_follows(num_users, config["avg_follows_per_user"])
    follows_csv_path = os.path.join(target_dir, "follows.csv")

    with open(follows_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["follower_id", "followee_id", "created_at"])
        for edge in follows:
            writer.writerow(edge)

    print(f"✅ Hoàn thành {len(follows):,} quan hệ Follows trong {time.time() - t0:.2f}s -> {follows_csv_path}")

    # ------------------------------------------------------------------------
    # 4. SINH DỮ LIỆU POSTS, POST_TAGS VÀ COMMENTS
    # ------------------------------------------------------------------------
    print(f"⏳ [4/5] Đang sinh Bài viết (Posts), Bình luận (Comments) và Gán Tag...")
    t0 = time.time()
    
    posts_csv_path = os.path.join(target_dir, "posts.csv")
    comments_csv_path = os.path.join(target_dir, "comments.csv")
    post_tags_csv_path = os.path.join(target_dir, "post_tags.csv")
    mongo_posts_jsonl_path = os.path.join(target_dir, "mongo_posts.jsonl")

    post_id_seq = 1
    comment_id_seq = 1

    with open(posts_csv_path, mode="w", newline="", encoding="utf-8") as f_post, \
         open(comments_csv_path, mode="w", newline="", encoding="utf-8") as f_comm, \
         open(post_tags_csv_path, mode="w", newline="", encoding="utf-8") as f_ptag, \
         open(mongo_posts_jsonl_path, mode="w", encoding="utf-8") as f_mongo:

        w_post = csv.writer(f_post)
        w_comm = csv.writer(f_comm)
        w_ptag = csv.writer(f_ptag)

        w_post.writerow(["id", "user_id", "content", "likes_count", "created_at"])
        w_comm.writerow(["id", "post_id", "user_id", "content", "created_at"])
        w_ptag.writerow(["post_id", "tag_id"])

        avg_posts = config["avg_posts_per_user"]
        avg_comments = config["avg_comments_per_post"]

        for user in users:
            uid = user["id"]
            num_posts = max(0, int(random.gauss(avg_posts, 1)))

            for _ in range(num_posts):
                pid = post_id_seq
                post_id_seq += 1

                # Chọn 1-3 tags ngẫu nhiên
                chosen_tags = random.sample(tags_list, k=random.randint(1, 3))
                primary_tag = chosen_tags[0]["name"]
                content = random.choice(POST_TEMPLATES).format(tag=primary_tag)
                likes = max(0, int(random.expovariate(1 / 20)))
                post_created_at = (base_time + timedelta(seconds=random.randint(30 * 86400, 90 * 86400))).isoformat() + "Z"

                # Ghi vào posts.csv
                w_post.writerow([pid, uid, content, likes, post_created_at])

                # Ghi vào post_tags.csv
                for tag in chosen_tags:
                    w_ptag.writerow([pid, tag["id"]])

                # Sinh bình luận cho bài viết này
                num_comments = max(0, int(random.gauss(avg_comments, 1.5)))
                embedded_comments = []

                for _ in range(num_comments):
                    cid = comment_id_seq
                    comment_id_seq += 1

                    commenter_id = random.randint(1, num_users)
                    comm_content = random.choice(COMMENT_TEMPLATES)
                    comm_created_at = (datetime.fromisoformat(post_created_at[:-1]) + timedelta(seconds=random.randint(60, 86400 * 5))).isoformat() + "Z"

                    # Ghi vào comments.csv (cho PostgreSQL / Neo4j)
                    w_comm.writerow([cid, pid, commenter_id, comm_content, comm_created_at])

                    # Gom vào mảng nhúng (cho MongoDB Document Model)
                    embedded_comments.append({
                        "comment_id": cid,
                        "user_id": commenter_id,
                        "content": comm_content,
                        "created_at": comm_created_at
                    })

                # Ghi Document đầy đủ vào mongo_posts.jsonl
                mongo_doc = {
                    "_id": pid,
                    "user_id": uid,
                    "content": content,
                    "likes_count": likes,
                    "tags": [t["name"] for t in chosen_tags],
                    "comments": embedded_comments,
                    "created_at": post_created_at
                }
                f_mongo.write(json.dumps(mongo_doc, ensure_ascii=False) + "\n")

    total_posts = post_id_seq - 1
    total_comments = comment_id_seq - 1
    print(f"✅ Hoàn thành {total_posts:,} Posts & {total_comments:,} Comments trong {time.time() - t0:.2f}s")

    # ------------------------------------------------------------------------
    # 5. TỔNG KẾT BỘ DỮ LIỆU
    # ------------------------------------------------------------------------
    total_elapsed = time.time() - start_total_time
    print(f"\n🎉 HOÀN THÀNH SINH DỮ LIỆU CHO QUY MÔ [{scale.upper()}] (Tổng thời gian: {total_elapsed:.2f}s):")
    print(f"   - Users:      {num_users:,} bản ghi")
    print(f"   - Follows:    {len(follows):,} quan hệ có hướng")
    print(f"   - Tags:       {len(TAG_POOL):,} nhãn")
    print(f"   - Posts:      {total_posts:,} bài viết")
    print(f"   - Comments:   {total_comments:,} bình luận")
    print(f"   - Files:      users.csv, tags.csv, follows.csv, posts.csv, comments.csv, post_tags.csv, mongo_posts.jsonl")
    print(f"========================================================\n")


def main():
    parser = argparse.ArgumentParser(description="Bộ sinh dữ liệu thực tế cho Đồ án Benchmark CSDL Phenikaa.")
    parser.add_argument(
        "--scale",
        type=str,
        default="small",
        choices=["test", "small", "medium", "large", "all"],
        help="Quy mô dữ liệu cần sinh: test (100 users), small (10K), medium (100K), large (500K), hoặc all (sinh cả 3)."
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "generated"),
        help="Thư mục lưu trữ dữ liệu xuất ra (mặc định: data/generated)."
    )

    args = parser.parse_args()

    if args.scale == "all":
        for sc in ["small", "medium", "large"]:
            generate_dataset(sc, args.output_dir)
    else:
        generate_dataset(args.scale, args.output_dir)


if __name__ == "__main__":
    main()
