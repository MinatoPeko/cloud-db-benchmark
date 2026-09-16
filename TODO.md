# 📋 DANH SÁCH CÔNG VIỆC DỰ ÁN (TODO LIST)

> **Đề tài:** Nghiên cứu, đánh giá hiệu năng các mô hình cơ sở dữ liệu quan hệ, phi quan hệ và đồ thị trên môi trường phát triển ảo hóa Cloud-based (GitHub Codespaces)  
> **Ngành:** Kỹ thuật Phần mềm - Đại học Phenikaa  
> **Thư mục dự án:** `C:\Users\ADMIN\Desktop\cloud-db-benchmark`  
> **Quy tắc cập nhật:** Mỗi khi hoàn thành hoặc bắt đầu một tác vụ, **bắt buộc** cập nhật trạng thái tại đây và ghi nhật ký tương ứng vào `PROGRESS.md`.

---

## 📊 TIẾN ĐỘ TỔNG THỂ

- **Tổng số công việc:** 37 đầu việc (9 Giai đoạn)
- **Đã hoàn thành:** 9 / 37 (24.3%)
- **Đang thực hiện:** 0
- **Chưa bắt đầu:** 28
- **Trạng thái quy ước:**
  - `[ ]` ⏳ Chưa bắt đầu (Todo)
  - `[/]` 🔄 Đang thực hiện (In Progress)
  - `[x]` ✅ Đã hoàn thành (Done)
  - `[-]` 🚫 Tạm hoãn / Hủy bỏ (Blocked/Dropped)

---

## 🚀 CHI TIẾT CÁC GIAI ĐOẠN

### GIAI ĐOẠN 1: Khởi tạo & Xác định Yêu cầu
- [x] **Task 1.1:** Khảo sát các tài liệu khoa học (IEEE, ACM) và bài báo so sánh hiệu năng SQL, NoSQL, Graph DB.
- [x] **Task 1.2:** Chốt thông số kỹ thuật môi trường đám mây GitHub Codespaces (gói vCPU, RAM, OS container).
- [x] **Task 1.3:** Soạn thảo bản Đề cương nghiên cứu chi tiết gửi Giảng viên hướng dẫn (GVHD).
- [x] **Task 1.4:** Khởi tạo cấu trúc repository GitHub, quy tắc commit, gitignore và README.md ban đầu.

---

### GIAI ĐOẠN 2: Thiết kế Mô hình Dữ liệu Đồng nhất
- [x] **Task 2.1:** Chốt chi tiết mô hình nghiệp vụ Mạng xã hội thực tế (User, Follow, Post, Comment, Tag).
- [x] **Task 2.2:** Thiết kế Schema CSDL Quan hệ (PostgreSQL: ERD, DDL, Khóa chính, Khóa ngoại, Constraints).
- [x] **Task 2.3:** Thiết kế Schema CSDL Tài liệu (MongoDB: JSON Schema, Collection design, Embedding vs Referencing).
- [x] **Task 2.4:** Thiết kế Schema CSDL Đồ thị (Neo4j: Property Graph Model, Node Labels, Relationship Types).
- [x] **Task 2.5:** Thiết kế chiến lược đánh chỉ mục (Index Strategy) tương đương và công bằng cho cả 3 CSDL.

---

### GIAI ĐOẠN 3: Xây dựng Hạ tầng "Một Thao Tác" trên Cloud (IaC)
- [ ] **Task 3.1:** Viết `docker-compose.yml` định nghĩa 3 dịch vụ CSDL (PostgreSQL 16, MongoDB 7.0, Neo4j 5.x).
- [ ] **Task 3.2:** Cấu hình thư mục `.devcontainer/devcontainer.json` để tự động hóa môi trường VS Code Codespaces.
- [ ] **Task 3.3:** Viết script kiểm tra trạng thái hoạt động (Healthcheck) của cả 3 CSDL sau khi khởi động.
- [ ] **Task 3.4:** Kiểm thử tính năng "One-Click / Một thao tác": Mở trực tiếp trên Codespaces kiểm tra độ ổn định.
- [ ] **Task 3.5:** Tích hợp huy hiệu "Open in GitHub Codespaces" vào `README.md`.

---

### GIAI ĐOẠN 4: Phát triển Bộ Sinh Dữ liệu & Nạp liệu (Data Pipeline)
- [ ] **Task 4.1:** Viết script sinh dữ liệu ngẫu nhiên thực tế `datagen.py` (Faker, NetworkX cho phân phối đồ thị thực tế).
- [ ] **Task 4.2:** Xuất dữ liệu ra các định dạng trung gian tiêu chuẩn (CSV và JSON).
- [ ] **Task 4.3:** Viết pipeline nhập liệu tự động (Data Ingestion) tối ưu cho PostgreSQL, MongoDB và Neo4j.
- [ ] **Task 4.4:** Sinh và chuẩn bị 3 bộ dữ liệu theo quy mô:
  - Small (10.000 thực thể)
  - Medium (100.000 thực thể)
  - Large (500.000 - 1.000.000 thực thể)
- [ ] **Task 4.5:** Viết script kiểm tra tính toàn vẹn (Data Checksum) đảm bảo số lượng dữ liệu ở 3 CSDL khớp nhau 100%.

---

### GIAI ĐOẠN 5: Xây dựng Công cụ Đo kiểm Hiệu năng (Benchmark Engine)
- [ ] **Task 5.1:** Soạn thảo danh mục truy vấn chi tiết theo 4 nhóm kịch bản (CRUD, Aggregate, Multi-hop Traversals, Stress).
- [ ] **Task 5.2:** Viết các câu truy vấn tương đương trên 3 ngôn ngữ: SQL (Postgres), MQL (Mongo), Cypher (Neo4j).
- [ ] **Task 5.3:** Xây dựng Benchmark Harness bằng Python (`benchmark_runner.py`) hỗ trợ:
  - Đo thời gian đáp ứng (Latency: Mean, p50, p95, p99).
  - Đo thông lượng (QPS/Throughput) dưới nhiều mức tải đồng thời (Concurrency).
  - Cơ chế xóa cache / Warm-up cache kiểm soát khoa học.
- [ ] **Task 5.4:** Tích hợp đo tài nguyên ảo hóa (CPU %, RAM MB, Disk I/O) qua thư viện `psutil` hoặc Docker stats.
- [ ] **Task 5.5:** Xuất kết quả đo lường tự động ra định dạng có cấu trúc (`results.json` / `results.csv`).

---

### GIAI ĐOẠN 6: Thực thi Đo đạc Thực nghiệm & Thu thập Số liệu
- [ ] **Task 6.1:** Thực nghiệm Nhóm 1 (CRUD & Bulk Write) trên 3 tập dữ liệu (lặp lại 5–10 lần, tính trung bình & độ lệch chuẩn).
- [ ] **Task 6.2:** Thực nghiệm Nhóm 2 (Aggregation, Filtering, Group By).
- [ ] **Task 6.3:** Thực nghiệm Nhóm 3 (Graph Traversals: 1-hop, 2-hop, 3-hop, 4-hop).
- [ ] **Task 6.4:** Thực nghiệm Nhóm 4 (Tài nguyên phần cứng, Cold Start vs Warm Cache).
- [ ] **Task 6.5:** Trích xuất Execution Plan (`EXPLAIN ANALYZE`, `.explain()`, `PROFILE`) để phục vụ giải thích chuyên sâu.

---

### GIAI ĐOẠN 7: Phân tích Dữ liệu, Trực quan hóa & Ma trận Khuyến nghị
- [ ] **Task 7.1:** Viết script Python (`visualize.py`) vẽ biểu đồ phân tích (Bar chart, Boxplot, Line chart, Heatmap).
- [ ] **Task 7.2:** Phân tích nguyên nhân gốc rễ (Root-cause analysis: Index-free Adjacency vs B-Tree Joins vs Document Lookups).
- [ ] **Task 7.3:** Xây dựng Bảng Ma trận Quyết định (Database Decision Matrix) phục vụ khuyến nghị thực tiễn cho kỹ sư phần mềm.

---

### GIAI ĐOẠN 8: Soạn thảo Toàn văn Báo cáo Đồ án (Chuẩn Phenikaa)
- [ ] **Task 8.1:** Viết Chương 1: Tổng quan đề tài & Mục tiêu nghiên cứu.
- [ ] **Task 8.2:** Viết Chương 2: Cơ sở lý thuyết về 3 mô hình CSDL và Ảo hóa Cloud (GitHub Codespaces).
- [ ] **Task 8.3:** Viết Chương 3: Thiết kế mô hình dữ liệu, hạ tầng container và kịch bản thực nghiệm.
- [ ] **Task 8.4:** Viết Chương 4: Kết quả thực nghiệm, đánh giá định lượng & Ma trận khuyến nghị.
- [ ] **Task 8.5:** Viết Chương 5: Kết luận, hạn chế và hướng phát triển.
- [ ] **Task 8.6:** Hoàn thiện Tài liệu tham khảo chuẩn IEEE, Danh mục bảng biểu, hình vẽ và Phụ lục mã nguồn.
- [ ] **Task 8.7:** Gửi bản thảo xin nhận xét của GVHD và chỉnh sửa theo góp ý.

---

### GIAI ĐOẠN 9: Đóng gói, Chuẩn bị Slide & Kịch bản Bảo vệ
- [ ] **Task 9.1:** Hoàn thiện `README.md`, dọn dẹp mã nguồn, đóng gói lệnh chạy thành script tự động (`run.sh` / `Makefile`).
- [ ] **Task 9.2:** Thiết kế Slide thuyết trình (15–20 slides súc tích, hình ảnh biểu đồ trực quan).
- [ ] **Task 9.3:** Xây dựng kịch bản Live Demo trực tiếp trên GitHub Codespaces trình diễn trước Hội đồng.
- [ ] **Task 9.4:** Tổng hợp bộ câu hỏi phản biện tiềm năng và câu trả lời dự phòng.
