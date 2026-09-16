# 🚀 Cloud-Based Multi-Model Database Performance Benchmarking

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new)
![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)
![Docker Compose](https://img.shields.io/badge/Docker%20Compose-v2-orange.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green.svg)
![Neo4j](https://img.shields.io/badge/Neo4j-5.x-lightblue.svg)

> **Đồ án Chuyên ngành Kỹ thuật Phần mềm - Trường Đại học Phenikaa**  
> **Đề tài:** Nghiên cứu, đánh giá hiệu năng các mô hình cơ sở dữ liệu quan hệ, phi quan hệ và đồ thị trên môi trường phát triển ảo hóa Cloud-based (GitHub Codespaces).

---

## 📌 1. Giới Thiệu Đề Tài (Project Overview)

Trong các hệ thống phần mềm quy mô lớn, việc lựa chọn giữa CSDL quan hệ (Relational), hướng tài liệu (Document) hay đồ thị (Graph) quyết định trực tiếp tới hiệu năng truy vấn, khả năng mở rộng và tài nguyên phần cứng.

Dự án này cung cấp một **khung thử nghiệm chuẩn hóa và tự động hóa 100% trên nền tảng Cloud (GitHub Codespaces)** nhằm so sánh định lượng:
- **PostgreSQL 16:** Đại diện CSDL Quan hệ (Relational - RDBMS).
- **MongoDB 7.0:** Đại diện CSDL Phi quan hệ / Hướng tài liệu (Document NoSQL).
- **Neo4j 5.x:** Đại diện CSDL Đồ thị (Property Graph Database).

Dựa trên bài toán thực tế **Mạng xã hội ảo (Social Network)** với 3 quy mô dữ liệu (**10K, 100K, 500K records**), hệ thống thực hiện đo đạc:
1. Thông lượng truy vấn (Throughput / QPS).
2. Thời gian đáp ứng (Latency: Mean, p50, p95, p99).
3. Tiêu hao tài nguyên ảo hóa Cloud (CPU %, RAM MB, Disk I/O).
4. Độ sâu quan hệ đa tầng (Graph Traversals từ 1-hop đến 4-hop).

---

## 🏗️ 2. Cấu Trúc Thư Mục Dự Án (Repository Structure)

```text
cloud-db-benchmark/
├── .devcontainer/              # Cấu hình tự động hóa môi trường GitHub Codespaces
│   ├── devcontainer.json       # Thiết lập VS Code Web, Extensions & Lifecycle hooks
│   └── Dockerfile              # Container image cho môi trường Benchmark Runner
├── data/                       # Dữ liệu thực nghiệm
│   ├── schemas/                # Lược đồ CSDL (SQL DDL, Mongo Validator, Cypher Constraints)
│   ├── generated/              # Dữ liệu giả lập xuất ra (CSV, JSON)
│   └── datagen.py              # Script sinh dữ liệu giả lập (Faker & NetworkX)
├── benchmarks/                 # Bộ công cụ đo kiểm hiệu năng (Benchmark Harness)
│   ├── queries/                # Danh mục truy vấn chuẩn hóa (SQL, MQL, Cypher)
│   ├── runner.py               # Benchmark engine thực thi tải và bấm giờ
│   └── monitor.py              # Trình giám sát tài nguyên CPU/RAM (psutil)
├── results/                    # Kết quả đo kiểm và trực quan hóa
│   ├── data/                   # File log kết quả thô (raw CSV/JSON)
│   ├── charts/                 # Biểu đồ phân tích xuất ra (300 DPI)
│   └── visualize.py            # Script vẽ biểu đồ (Matplotlib & Seaborn)
├── docker-compose.yml          # Hạ tầng 3 CSDL (PostgreSQL, MongoDB, Neo4j)
├── requirements.txt            # Thư viện Python phụ thuộc
├── .gitignore                  # Cấu hình bỏ qua các file tạm, log, dataset lớn
├── README.md                   # Tài liệu hướng dẫn chính của Repository
├── TODO.md                     # Danh sách 37 đầu việc & tiến độ tổng thể (WBS)
├── PROGRESS.md                 # Nhật ký tiến trình thực hiện theo thời gian thực
├── explain.md                  # Bản giải thích chi tiết về bản chất và cách hoạt động
├── TAI_LIEU_KHAO_SAT.md        # Tổng hợp 6 nghiên cứu khoa học tiền đề IEEE/ACM
└── DE_CUONG_DO_AN.md           # Bản Đề cương chi tiết nộp Giảng viên hướng dẫn
```

---

## ⚡ 3. Hướng Dẫn Khởi Động "Một Thao Tác" (Quickstart on Codespaces)

Nhờ cơ chế **Infrastructure as Code (IaC)**, bạn không cần cài đặt bất kỳ phần mềm nào vào máy tính cá nhân:

1. Click vào huy hiệu **[Open in GitHub Codespaces](https://github.com/codespaces/new)** ở đầu trang.
2. Chọn máy ảo cấu hình **4 cores, 16 GB RAM**.
3. Codespaces sẽ tự động khởi động và chạy nền toàn bộ 3 CSDL qua `docker-compose.yml`:
   - **PostgreSQL 16:** Cổng `5432`
   - **MongoDB 7.0:** Cổng `27017`
   - **Neo4j 5.x:** Cổng `7474` (Web Browser) & `7687` (Bolt Protocol)
4. Mở Terminal trong VS Code và gõ lệnh chạy kiểm thử:
   ```bash
   # 1. Sinh dữ liệu mẫu quy mô nhỏ (Small: 10k entities)
   python data/datagen.py --scale small

   # 2. Nạp dữ liệu vào cả 3 database
   python data/import_all.py --scale small

   # 3. Chạy toàn bộ kịch bản benchmark
   python benchmarks/runner.py --all

   # 4. Trực quan hóa và xuất biểu đồ kết quả
   python results/visualize.py
   ```

---

## 📖 4. Tài Liệu Nghiên Cứu & Quản Lý Dự Án

- **Đề cương chi tiết nộp GVHD:** Xem [DE_CUONG_DO_AN.md](DE_CUONG_DO_AN.md)
- **Cơ sở khoa học & Trích dẫn IEEE/ACM:** Xem [TAI_LIEU_KHAO_SAT.md](TAI_LIEU_KHAO_SAT.md)
- **Tiến độ công việc (TODO):** Xem [TODO.md](TODO.md)
- **Nhật ký tiến trình thời gian thực:** Xem [PROGRESS.md](PROGRESS.md)
- **Giải thích trực quan bản chất đề tài:** Xem [explain.md](explain.md)

---

## 👨‍💻 Tác Giả & Đơn Vị Đào Tạo
- **Sinh viên thực hiện:** `[Họ và tên sinh viên]` (`[Mã sinh viên]`)
- **Ngành:** Kỹ thuật Phần mềm - Khoa Công nghệ Thông tin
- **Trường:** Trường Đại học Phenikaa (Phenikaa University)
- **Giảng viên hướng dẫn:** `[TS/ThS. Giảng viên hướng dẫn]`
