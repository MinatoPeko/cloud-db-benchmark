#!/usr/bin/env python3
"""
tools/render_diagrams.py
Tạo 6 sơ đồ kiến trúc chất lượng cao 300 DPI, căn chỉnh toạ độ chính xác tuyệt đối,
không bao giờ bị đè chữ (overlap).
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

os.environ["MPLCONFIGDIR"] = os.path.join(os.environ.get("TEMP", os.path.expanduser("~")), "matplotlib_cache")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "results", "diagrams")
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Segoe UI', 'sans-serif']
plt.rcParams['font.family'] = 'sans-serif'


def render_diagram_1():
    """Hình 1.1: Sơ đồ luồng phương pháp luận nghiên cứu 5 bước"""
    fig, ax = plt.subplots(figsize=(10.5, 11.5), dpi=300)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 11.5)
    ax.axis("off")

    steps = [
        ("1. Nghiên cứu Lý thuyết & Khoa học Tiền đề",
         ["Khảo sát 6 công trình học thuật chuẩn quốc tế IEEE / ACM",
          "Phân tích Storage Engines: B-Tree, WiredTiger, Index-Free Adjacency",
          "Nhận diện khoảng trống nghiên cứu (Research Gap) và mục tiêu đề tài"],
         "#EFF6FF", "#2563EB"),

        ("2. Mô hình hóa Kỹ thuật Phần mềm",
         ["Đặc tả 7 Ca sử dụng (Use Cases UC-01 đến UC-07) & Ma trận truy vết",
          "Thiết kế Lược đồ dữ liệu đồng nhất: 3NF SQL, BSON nhúng, Property Graph",
          "Thiết lập chiến lược đánh chỉ mục tương đương và công bằng"],
         "#F0FDF4", "#16A34A"),

        ("3. Thực nghiệm Đo kiểm Định lượng (Empirical Benchmark)",
         ["Khởi tạo hạ tầng 1-Click trên Cloud (GitHub Codespaces Dev Container)",
          "Sinh dữ liệu Barabási–Albert phản ánh mạng xã hội thực tế (10.000 users)",
          "Đo kiểm tải 20 vòng lặp, kiểm soát bộ đệm (Warm-up vs Cold Cache)"],
         "#FEF3C7", "#D97706"),

        ("4. Phân tích Nguyên nhân Gốc rễ (Root-Cause Analysis)",
         ["Trích xuất kế hoạch thực thi: EXPLAIN ANALYZE, .explain(), PROFILE",
          "Giải mã lý do MongoDB p99 siêu thấp (5.77ms) & Postgres In-Memory",
          "Giải thích chi phí overhead nền của máy ảo Java (JVM) và Bolt trên Neo4j"],
         "#F3E8FF", "#9333EA"),

        ("5. Tổng hợp Tri thức & Xây dựng Ma trận Quyết định",
         ["Trực quan hóa hệ thống 4 biểu đồ phân tích thực nghiệm chuẩn 300 DPI",
          "Xây dựng Bảng Ma trận Quyết định Lựa chọn CSDL (Database Decision Matrix)",
          "Đề xuất định hướng kiến trúc Đa mô hình lưu trữ (Polyglot Persistence)"],
         "#ECFEFF", "#0891B2")
    ]

    box_w = 9.2
    box_h = 1.65
    start_x = 0.65
    y_positions = [9.4, 7.15, 4.9, 2.65, 0.4]

    for idx, (title, items, bg_col, border_col) in enumerate(steps):
        cur_y = y_positions[idx]
        
        # Hộp nền bo góc
        box = FancyBboxPatch((start_x, cur_y), box_w, box_h,
                             boxstyle="round,pad=0.03,rounding_size=0.04",
                             facecolor=bg_col, edgecolor=border_col, linewidth=2, zorder=2)
        ax.add_patch(box)

        # Thanh tiêu đề phụ bên trong hộp
        header_h = 0.45
        header_y = cur_y + box_h - header_h
        ax.plot([start_x + 0.1, start_x + box_w - 0.1], [header_y, header_y],
                color=border_col, lw=1.2, zorder=3)

        # Chữ tiêu đề: căn giữa hoàn hảo trong thanh tiêu đề
        ax.text(start_x + box_w/2, cur_y + box_h - 0.25, title,
                ha="center", va="center", fontsize=11.5, fontweight="bold",
                color="#0F172A", zorder=4)

        # Các dòng nội dung gạch đầu dòng: bắt đầu bên dưới thanh tiêu đề
        content_top = header_y - 0.22
        line_spacing = 0.32
        for i_itm, itm in enumerate(items):
            ax.text(start_x + 0.3, content_top - i_itm * line_spacing, f"•  {itm}",
                    ha="left", va="center", fontsize=10.0, color="#1E293B", zorder=4)

        # Mũi tên kết nối xuống bước tiếp theo
        if idx < len(steps) - 1:
            arrow_x = start_x + box_w / 2
            next_y = y_positions[idx + 1]
            ax.annotate("", xy=(arrow_x, next_y + box_h + 0.05), xytext=(arrow_x, cur_y - 0.05),
                        arrowprops=dict(arrowstyle="-|>", lw=2.2, color="#475569", mutation_scale=16))

    out_path = os.path.join(OUTPUT_DIR, "hinh_1_1_phuong_phap_luan.png")
    fig.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"✅ Đã render thành công: {out_path}")


def render_diagram_2():
    """Hình 2.1: So sánh 3 Trường phái Kiến trúc CSDL"""
    fig, ax = plt.subplots(figsize=(11.5, 5.5), dpi=300)
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 5.5)
    ax.axis("off")

    cards = [
        ("1. CSDL Quan hệ (Relational)", "#EFF6FF", "#2563EB", [
            "Mô hình bảng 2 chiều (Dòng & Cột)",
            "Nền tảng Đại số quan hệ (Codd 1970)",
            "Chuẩn hóa dữ liệu chặt chẽ (3NF)",
            "Ràng buộc toàn vẹn khóa ngoại (PK/FK)",
            "Bảo đảm 4 thuộc tính ACID nghiêm ngặt",
            "Nối bảng JOIN thời gian thực (Runtime)",
            "Phù hợp: Giao dịch tài chính, dữ liệu cố định"
        ]),
        ("2. CSDL Hướng tài liệu (Document)", "#F0FDF4", "#16A34A", [
            "Mô hình cây tài liệu BSON bán cấu trúc",
            "Lược đồ linh hoạt (Flexible Schema)",
            "Nhúng mảng bình luận & thẻ vào bài viết",
            "Triệt tiêu hoàn toàn phép nối JOIN",
            "Tối ưu đọc phân cấp & ghi hàng loạt",
            "Độ trễ p99 siêu ổn định (5.77ms)",
            "Phù hợp: Content web, luồng feeds, catalog"
        ]),
        ("3. CSDL Đồ thị thuộc tính (Graph)", "#FAF5FF", "#9333EA", [
            "Mô hình mạng lưới Đỉnh (Nodes) & Cạnh",
            "Quan hệ có hướng mang thuộc tính phong phú",
            "Duyệt trực tiếp Index-Free Adjacency",
            "Con trỏ bộ nhớ hai chiều giữa các nút",
            "Độ phức tạp O(k) độc lập tổng số dữ liệu",
            "Tối ưu truy vấn quan hệ đa tầng (n-hop)",
            "Phù hợp: Mạng xã hội, gợi ý, gian lận"
        ])
    ]

    card_w = 3.4
    card_h = 4.8
    start_x = 0.4
    spacing = 0.35
    y = 0.35

    for i, (title, bg, border, items) in enumerate(cards):
        x = start_x + i * (card_w + spacing)
        
        box = FancyBboxPatch((x, y), card_w, card_h,
                             boxstyle="round,pad=0.03,rounding_size=0.04",
                             facecolor=bg, edgecolor=border, linewidth=2, zorder=2)
        ax.add_patch(box)

        # Header bar
        header_h = 0.65
        header_y = y + card_h - header_h
        ax.plot([x + 0.1, x + card_w - 0.1], [header_y, header_y], color=border, lw=1.2, zorder=3)

        ax.text(x + card_w/2, y + card_h - 0.35, title,
                ha="center", va="center", fontsize=11, fontweight="bold", color="#0F172A", zorder=4)

        content_top = header_y - 0.3
        line_spacing = 0.52
        for i_itm, itm in enumerate(items):
            ax.text(x + 0.18, content_top - i_itm * line_spacing, f"• {itm}",
                    ha="left", va="center", fontsize=9.5, color="#1E293B", zorder=4)

    out_path = os.path.join(OUTPUT_DIR, "hinh_2_1_3_paradigms.png")
    fig.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"✅ Đã render thành công: {out_path}")


def render_diagram_3():
    """Hình 2.2: So sánh Kiến trúc Động cơ Lưu trữ & Truy xuất (Storage Engines)"""
    fig, ax = plt.subplots(figsize=(11.5, 5.5), dpi=300)
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 5.5)
    ax.axis("off")

    engines = [
        ("PostgreSQL 16 (Relational)", "#F8FAFC", "#0284C7", [
            "Kiến trúc tệp đống Heap Files",
            "Kích thước trang đĩa cố định: 8 KB",
            "Bộ đệm bộ nhớ: Shared Buffers Pool",
            "Cấu trúc chỉ mục: B-Tree (Lehman-Yao)",
            "Kiểm soát tương tranh: MVCC (xmin/xmax)",
            "Ghi nhật ký trước: Write-Ahead Log (WAL)",
            "Thu hồi rác đĩa ngầm: Tiến trình VACUUM"
        ]),
        ("MongoDB 7.0 (WiredTiger)", "#F8FAFC", "#10B981", [
            "Động cơ lưu trữ WiredTiger Engine",
            "Bộ nhớ đệm người dùng: WiredTiger Cache (2GB)",
            "Nén khối đĩa mặc định: Snappy / zlib",
            "Chỉ mục mảng: Multikey B-Tree Index",
            "Cơ chế an toàn: Journaling & Checkpoints",
            "Hỗ trợ giao dịch Multi-document ACID",
            "Ghi hàng loạt cực nhanh (Bulk Ingestion)"
        ]),
        ("Neo4j 5.x (Native Graph)", "#F8FAFC", "#8B5CF6", [
            "Lưu trữ bản ghi cố định (Record-based)",
            "Đỉnh: 15 Bytes | Cạnh quan hệ: 34 Bytes",
            "Bộ đệm: Pagecache (2GB) + JVM Heap (2GB)",
            "Duyệt trực tiếp: Index-Free Adjacency",
            "Danh sách liên kết kép 2 chiều (Pointers)",
            "Ngôn ngữ truy vấn đồ thị: Cypher",
            "Giao thức nhị phân kết nối: Bolt Protocol"
        ])
    ]

    card_w = 3.4
    card_h = 4.8
    start_x = 0.4
    spacing = 0.35
    y = 0.35

    for i, (title, bg, border, items) in enumerate(engines):
        x = start_x + i * (card_w + spacing)
        
        box = FancyBboxPatch((x, y), card_w, card_h,
                             boxstyle="round,pad=0.03,rounding_size=0.04",
                             facecolor=bg, edgecolor=border, linewidth=2, zorder=2)
        ax.add_patch(box)

        header_h = 0.65
        header_y = y + card_h - header_h
        ax.plot([x + 0.1, x + card_w - 0.1], [header_y, header_y], color=border, lw=1.2, zorder=3)

        ax.text(x + card_w/2, y + card_h - 0.35, title,
                ha="center", va="center", fontsize=11, fontweight="bold", color="#0F172A", zorder=4)

        content_top = header_y - 0.3
        line_spacing = 0.52
        for i_itm, itm in enumerate(items):
            ax.text(x + 0.18, content_top - i_itm * line_spacing, f"• {itm}",
                    ha="left", va="center", fontsize=9.5, color="#1E293B", zorder=4)

    out_path = os.path.join(OUTPUT_DIR, "hinh_2_2_engine_comparison.png")
    fig.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"✅ Đã render thành công: {out_path}")


def render_diagram_4():
    """Hình 2.3: Kiến trúc Hạ tầng Ảo hóa Cloud Dev Container"""
    fig, ax = plt.subplots(figsize=(11.0, 5.8), dpi=300)
    ax.set_xlim(0, 11.0)
    ax.set_ylim(0, 5.8)
    ax.axis("off")

    # Client
    box_client = FancyBboxPatch((0.4, 2.1), 2.3, 1.8, boxstyle="round,pad=0.03,rounding_size=0.04",
                                facecolor="#EFF6FF", edgecolor="#2563EB", linewidth=2)
    ax.add_patch(box_client)
    ax.text(1.55, 3.4, "Kỹ sư / Nhà Nghiên cứu", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#1E3A8A")
    ax.text(1.55, 2.7, "Chỉ cần Trình duyệt Web\nhoặc VS Code Web\n(1-Click Open Codespace)", ha="center", va="center", fontsize=9, color="#475569")

    # Mũi tên kết nối
    ax.annotate("", xy=(3.5, 3.0), xytext=(2.7, 3.0),
                arrowprops=dict(arrowstyle="-|>", lw=2.2, color="#2563EB", mutation_scale=15))
    ax.text(3.1, 3.25, "HTTPS", ha="center", fontsize=9, fontweight="bold", color="#2563EB")

    # Khung Cloud Codespaces
    box_cloud = FancyBboxPatch((3.5, 0.4), 7.1, 5.0, boxstyle="round,pad=0.03,rounding_size=0.04",
                               facecolor="#F8FAFC", edgecolor="#475569", linewidth=2, linestyle="--")
    ax.add_patch(box_cloud)
    ax.text(7.05, 5.15, "Hạ tầng GitHub Codespaces Cloud VM (4 vCPUs, 16 GB RAM, 32 GB SSD, Ubuntu)",
            ha="center", va="center", fontsize=10.5, fontweight="bold", color="#0F172A")

    # Khung Mạng Docker Bridge
    box_net = FancyBboxPatch((3.8, 0.7), 6.5, 4.0, boxstyle="round,pad=0.03,rounding_size=0.03",
                            facecolor="#F1F5F9", edgecolor="#94A3B8", linewidth=1.5)
    ax.add_patch(box_net)
    ax.text(7.05, 4.45, "Mạng Ảo hóa Nội bộ Docker Bridge: 'benchmark-net'", ha="center", va="center",
            fontsize=9.5, fontweight="bold", color="#334155")

    # 4 Containers chi tiết
    containers = [
        (4.0, 2.65, 2.9, 1.55, "#FFFFFF", "#3B82F6", "workspace (Python 3.11)", [
            "Benchmark Runner Engine", "psutil Resource Monitor", "Drivers: psycopg2, pymongo, neo4j"
        ]),
        (7.2, 2.65, 2.9, 1.55, "#FFFFFF", "#0284C7", "postgres (Port 5432)", [
            "PostgreSQL 16.15-alpine", "Limit: 3 GB RAM", "Shared Buffers Pool (RAM Cache)"
        ]),
        (4.0, 0.95, 2.9, 1.55, "#FFFFFF", "#10B981", "mongo (Port 27017)", [
            "MongoDB 7.0 Community", "Limit: 4 GB RAM", "WiredTiger Cache: 2 GB"
        ]),
        (7.2, 0.95, 2.9, 1.55, "#FFFFFF", "#8B5CF6", "neo4j (Port 7687 Bolt)", [
            "Neo4j 5.26 Community", "Limit: 5 GB RAM", "Heap: 2GB | Pagecache: 2GB"
        ])
    ]

    for cx, cy, cw, ch, cbg, cborder, ctitle, citms in containers:
        cbox = FancyBboxPatch((cx, cy), cw, ch, boxstyle="round,pad=0.02,rounding_size=0.03",
                              facecolor=cbg, edgecolor=cborder, linewidth=1.5, zorder=3)
        ax.add_patch(cbox)

        cheader_h = 0.38
        cheader_y = cy + ch - cheader_h
        ax.plot([cx + 0.08, cx + cw - 0.08], [cheader_y, cheader_y], color=cborder, lw=1, zorder=4)

        ax.text(cx + cw/2, cy + ch - 0.2, ctitle,
                ha="center", va="center", fontsize=9.5, fontweight="bold", color="#0F172A", zorder=5)

        for i_it, it in enumerate(citms):
            ax.text(cx + 0.12, cheader_y - 0.22 - i_it * 0.32, f"• {it}",
                    ha="left", va="center", fontsize=8.5, color="#334155", zorder=5)

    out_path = os.path.join(OUTPUT_DIR, "hinh_2_3_devcontainer_stack.png")
    fig.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"✅ Đã render thành công: {out_path}")


def render_diagram_5():
    """Hình 3.1: Sơ đồ ERD Miền Mạng Xã Hội"""
    fig, ax = plt.subplots(figsize=(11.0, 6.5), dpi=300)
    ax.set_xlim(0, 11.0)
    ax.set_ylim(0, 6.5)
    ax.axis("off")

    entities = [
        (0.6, 3.8, 2.8, 2.2, "#EFF6FF", "#2563EB", "USERS", [
            "id: BIGINT (PK)", "username: VARCHAR(50) (UK)", "email: VARCHAR(100) (UK)", "full_name: VARCHAR(100)", "created_at: TIMESTAMP"
        ]),
        (0.6, 0.8, 2.8, 2.0, "#F0FDF4", "#16A34A", "FOLLOWS (Graph)", [
            "follower_id: BIGINT (PK, FK)", "followee_id: BIGINT (PK, FK)", "created_at: TIMESTAMP", "CHECK (follower <> followee)"
        ]),
        (4.2, 3.8, 2.8, 2.2, "#FEF3C7", "#D97706", "POSTS", [
            "id: BIGINT (PK)", "user_id: BIGINT (FK)", "content: TEXT", "likes_count: INTEGER", "created_at: TIMESTAMP"
        ]),
        (4.2, 0.8, 2.8, 2.0, "#F3E8FF", "#9333EA", "COMMENTS", [
            "id: BIGINT (PK)", "post_id: BIGINT (FK)", "user_id: BIGINT (FK)", "content: TEXT", "created_at: TIMESTAMP"
        ]),
        (7.8, 4.0, 2.6, 1.8, "#ECFEFF", "#0891B2", "TAGS", [
            "id: SERIAL (PK)", "name: VARCHAR(50) (UK)"
        ]),
        (7.8, 1.0, 2.6, 1.8, "#FFF1F2", "#E11D48", "POST_TAGS (N-N)", [
            "post_id: BIGINT (PK, FK)", "tag_id: INTEGER (PK, FK)"
        ])
    ]

    for ex, ey, ew, eh, ebg, eborder, etitle, eitms in entities:
        box = FancyBboxPatch((ex, ey), ew, eh, boxstyle="round,pad=0.03,rounding_size=0.04",
                             facecolor=ebg, edgecolor=eborder, linewidth=1.8, zorder=2)
        ax.add_patch(box)

        eh_h = 0.42
        eh_y = ey + eh - eh_h
        ax.plot([ex + 0.08, ex + ew - 0.08], [eh_y, eh_y], color=eborder, lw=1.2, zorder=3)

        ax.text(ex + ew/2, ey + eh - 0.22, etitle,
                ha="center", va="center", fontsize=10.5, fontweight="bold", color="#0F172A", zorder=4)

        for i_it, it in enumerate(eitms):
            ax.text(ex + 0.15, eh_y - 0.22 - i_it * 0.32, f"• {it}",
                    ha="left", va="center", fontsize=8.5, color="#1E293B", zorder=4)

    # Đường nối quan hệ
    ax.annotate("", xy=(2.0, 2.8), xytext=(2.0, 3.8), arrowprops=dict(arrowstyle="<->", lw=1.8, color="#475569"))
    ax.text(2.1, 3.3, "1 - N (Follows)", fontsize=9, color="#475569", fontweight="bold")

    ax.annotate("", xy=(4.2, 4.9), xytext=(3.4, 4.9), arrowprops=dict(arrowstyle="->", lw=1.8, color="#475569"))
    ax.text(3.6, 5.1, "authors", fontsize=9, color="#475569", fontweight="bold")

    ax.annotate("", xy=(5.6, 3.8), xytext=(5.6, 2.8), arrowprops=dict(arrowstyle="->", lw=1.8, color="#475569"))
    ax.text(5.7, 3.3, "contains", fontsize=9, color="#475569", fontweight="bold")

    ax.annotate("", xy=(7.8, 4.9), xytext=(7.0, 4.9), arrowprops=dict(arrowstyle="->", lw=1.8, color="#475569"))

    ax.annotate("", xy=(9.1, 4.0), xytext=(9.1, 2.8), arrowprops=dict(arrowstyle="->", lw=1.8, color="#475569"))
    ax.text(9.2, 3.4, "links", fontsize=9, color="#475569", fontweight="bold")

    out_path = os.path.join(OUTPUT_DIR, "hinh_3_1_erd_social_network.png")
    fig.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"✅ Đã render thành công: {out_path}")


def render_diagram_6():
    """Hình 3.5: Trình tự Đo kiểm và Giám sát Tài nguyên (Sequence Diagram)"""
    fig, ax = plt.subplots(figsize=(11.0, 6.8), dpi=300)
    ax.set_xlim(0, 11.0)
    ax.set_ylim(0, 6.8)
    ax.axis("off")

    lifelines = [
        (1.9, "Benchmark Runner\n(runner.py)", "#2563EB"),
        (5.5, "Resource Monitor\n(monitor.py Thread)", "#16A34A"),
        (9.1, "Target DBMS\n(Postgres / Mongo / Neo4j)", "#9333EA")
    ]

    for lx, label, col in lifelines:
        box = FancyBboxPatch((lx - 1.25, 5.9), 2.5, 0.75, boxstyle="round,pad=0.03,rounding_size=0.03",
                             facecolor="#F8FAFC", edgecolor=col, linewidth=1.8)
        ax.add_patch(box)
        ax.text(lx, 6.27, label, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#0F172A")
        ax.plot([lx, lx], [0.6, 5.9], color="#CBD5E1", lw=1.8, linestyle="--")

    messages = [
        (5.3, 1.9, 9.1, "1. Khởi động Warm-up Phase (Gửi truy vấn mồi nạp Buffer Cache)", "->", "#2563EB"),
        (4.7, 1.9, 5.5, "2. Kích hoạt lấy mẫu tài nguyên ngầm định kỳ 0.5s (start())", "->", "#059669"),
        (4.0, 1.9, 9.1, "3. Vòng lặp 20 lần: Bắn tải truy vấn (SQL / MQL / Cypher)", "->", "#0F172A"),
        (3.4, 9.1, 1.9, "4. Trả kết quả hoàn chỉnh & Bấm giờ nano-giây (time.perf_counter)", "-->", "#64748B"),
        (2.7, 1.9, 5.5, "5. Dừng luồng lấy mẫu tài nguyên hệ thống (stop())", "->", "#059669"),
        (2.1, 5.5, 1.9, "6. Trả về thống kê: CPU Mean %, RAM Peak MB, Disk I/O MB", "-->", "#059669"),
        (1.5, 1.9, 1.9, "7. Tính toán phân vị: Mean, p50, p95, p99, Throughput QPS", "loop", "#2563EB"),
        (0.9, 1.9, 1.9, "8. Xuất bảng dữ liệu chuẩn hoá CSV: results/data/*.csv", "loop", "#0F172A")
    ]

    for y, x1, x2, text, style, col in messages:
        if style == "->":
            ax.annotate("", xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle="-|>", lw=1.8, color=col, mutation_scale=13))
            ax.text((x1 + x2)/2, y + 0.12, text, ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=col)
        elif style == "-->":
            ax.annotate("", xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle="-|>", lw=1.8, color=col, linestyle="--", mutation_scale=13))
            ax.text((x1 + x2)/2, y + 0.12, text, ha="center", va="bottom", fontsize=8.5, color=col)
        elif style == "loop":
            ax.plot([x1, x1 + 0.7, x1 + 0.7, x1], [y + 0.16, y + 0.16, y - 0.16, y - 0.16], color=col, lw=1.8)
            ax.annotate("", xy=(x1, y - 0.16), xytext=(x1 + 0.12, y - 0.16),
                        arrowprops=dict(arrowstyle="-|>", lw=1.8, color=col, mutation_scale=11))
            ax.text(x1 + 0.82, y, text, ha="left", va="center", fontsize=8.5, fontweight="bold", color=col)

    out_path = os.path.join(OUTPUT_DIR, "hinh_3_5_sequence_benchmark.png")
    fig.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"✅ Đã render thành công: {out_path}")


if __name__ == "__main__":
    print("🎨 Đang render lại toàn bộ 6 sơ đồ với toạ độ căn chỉnh tuyệt đối...")
    render_diagram_1()
    render_diagram_2()
    render_diagram_3()
    render_diagram_4()
    render_diagram_5()
    render_diagram_6()
    print("🎉 Hoàn tất 6/6 sơ đồ hoàn hảo!")
