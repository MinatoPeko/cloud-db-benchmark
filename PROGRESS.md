# ⏱️ NHẬT KÝ TIẾN TRÌNH DỰ ÁN (PROJECT PROGRESS LOG)

> **Mục đích:** Ghi lại toàn bộ lịch sử triển khai, các mốc hoàn thành, quyết định kỹ thuật và các thay đổi mã nguồn theo thời gian thực.  
> **Thư mục dự án:** `C:\Users\ADMIN\Desktop\cloud-db-benchmark`  
> **Quy tắc phối hợp:** Mỗi khi hoàn thành bất kỳ tác vụ nào:
> 1. Đánh dấu `[x]` vào đầu việc tương ứng trong `TODO.md`.
> 2. Ghi thêm một mục nhật ký (Entry) mới vào cuối file này theo mẫu chuẩn.

---

## 📌 QUY CHUẨN MẪU GHI NHẬT KÝ (LOG ENTRY TEMPLATE)

```markdown
### [YYYY-MM-DD HH:mm] - [Tên Tác Vụ hoặc Mã Task]
- **Trạng thái:** ✅ Hoàn thành / 🔄 Đang thực hiện / ⚠️ Gặp vướng mắc
- **Công việc đã thực hiện:**
  - Chi tiết công việc 1
  - Chi tiết công việc 2
- **Tài liệu / Mã nguồn liên quan:**
  - `path/to/file1.ext` (Tạo mới / Cập nhật)
- **Quyết định kỹ thuật / Phát hiện:** (Nếu có)
- **Bước tiếp theo cần làm:** Tên tác vụ kế tiếp trong TODO.md
```

---

## 📜 LỊCH SỬ TIẾN TRÌNH THEO THỜI GIAN THỰC

### [2026-09-10 13:25] - Khởi tạo Dự án & Thiết lập Quy trình Quản lý
- **Trạng thái:** ✅ Hoàn thành
- **Công việc đã thực hiện:**
  - Thống nhất đề tài đồ án chuyên ngành KTPM Phenikaa: *"Nghiên cứu, đánh giá hiệu năng các mô hình cơ sở dữ liệu quan hệ, phi quan hệ và đồ thị trên môi trường phát triển ảo hóa Cloud-based (GitHub Codespaces)"*.
  - Đối chiếu và xác nhận độ tương thích 100% với phiếu đề xuất đề tài được phê duyệt.
  - Phân rã công việc (WBS) thành 9 giai đoạn chuẩn mực và 37 đầu việc chi tiết trong `TODO.md`.
  - Thiết lập cơ chế ghi nhật ký tiến trình thời gian thực trong `PROGRESS.md`.
- **Tài liệu / Mã nguồn liên quan:**
  - `TODO.md`: Khởi tạo danh sách 37 task chi tiết.
  - `PROGRESS.md`: Khởi tạo nhật ký theo dõi thời gian thực.
  - `implementation_plan.md`: Bản kế hoạch kỹ thuật tổng thể.
- **Quyết định kỹ thuật cốt lõi:**
  - Stack CSDL: PostgreSQL 16, MongoDB 7.0, Neo4j 5.x.
  - Nền tảng ảo hóa: GitHub Codespaces kết hợp Dev Containers (`.devcontainer` + `docker-compose`).
  - Bài toán dữ liệu: Mạng xã hội thu nhỏ (Social Network Graph) với 3 mức độ quy mô (10K, 100K, 500K - 1M).

### [2026-09-10 13:28] - Chuyển Không Gian Làm Việc Sang Desktop/Do_an
- **Trạng thái:** ✅ Hoàn thành
- **Công việc đã thực hiện:**
  - Di chuyển và thiết lập không gian làm việc chính thức tại: `C:\Users\ADMIN\Desktop\Do_an`.
  - Đồng bộ hóa các tài liệu quản lý dự án (`TODO.md`, `PROGRESS.md`) vào thư mục mới.
- **Tài liệu / Mã nguồn liên quan:**
  - `C:\Users\ADMIN\Desktop\Do_an\TODO.md`
  - `C:\Users\ADMIN\Desktop\Do_an\PROGRESS.md`
- **Bước tiếp theo cần làm:** Lựa chọn tác vụ bắt đầu triển khai (Giai đoạn 3: Hạ tầng Container hay Giai đoạn 2: Thiết kế Schema hay Giai đoạn 1: Đề cương).

### [2026-09-12 10:28] - Lưu Tài Liệu Giải Thích Bản Chất Dự Án (explain.md)
- **Trạng thái:** ✅ Hoàn thành
- **Công việc đã thực hiện:**
  - Soạn thảo tài liệu giải thích chi tiết, trực quan về bản chất dự án, so sánh 3 trường phái CSDL (PostgreSQL, MongoDB, Neo4j).
  - Trình bày luồng vận hành khép kín 5 bước (Khởi tạo 1-click -> Cấp phát dữ liệu -> Bắn tải benchmark -> Giám sát tài nguyên -> Trực quan hóa & Khuyến nghị) kèm sơ đồ Mermaid.
  - Phân tích 3 bài toán thực nghiệm và làm rõ các sản phẩm bàn giao (Deliverables) của đồ án.
  - Lưu trữ tài liệu vào file `explain.md`.
- **Tài liệu / Mã nguồn liên quan:**
  - `C:\Users\ADMIN\Desktop\Do_an\explain.md` (Tạo mới)
- **Bước tiếp theo cần làm:** Bắt đầu triển khai Giai đoạn 1 theo chỉ đạo của người dùng.

### [2026-09-12 10:45] - Hoàn Thành Giai Đoạn 1: Khởi Tạo & Xác Định Yêu Cầu (Task 1.1 - 1.4)
- **Trạng thái:** ✅ Hoàn thành
- **Công việc đã thực hiện:**
  - **Task 1.1:** Khảo sát và tổng hợp 6 công trình nghiên cứu khoa học tiền đề chuẩn IEEE/ACM/Springer về so sánh SQL, NoSQL và Graph DB; phân tích khoảng trống nghiên cứu (Research Gap) và ma trận đặc tính kỹ thuật.
  - **Task 1.2:** Chốt thông số kỹ thuật môi trường ảo hóa GitHub Codespaces theo lựa chọn người dùng: **4 vCPUs, 16 GB RAM, 32 GB SSD Storage**, Linux container.
  - **Task 1.3:** Soạn thảo bản Đề cương nghiên cứu chi tiết chuẩn Khoa CNTT - Bộ môn KTPM Đại học Phenikaa (gồm 6 mục lớn, kế hoạch 10 tuần, sử dụng placeholder thông tin cá nhân).
  - **Task 1.4:** Khởi tạo cấu trúc dự án chuẩn, file `.gitignore` chuyên nghiệp, file `README.md` tích hợp huy hiệu "Open in GitHub Codespaces", và các thư mục với marker `.gitkeep`.
  - Cập nhật tiến độ trong `TODO.md` đạt **4/37 tasks (10.8%)**.
- **Tài liệu / Mã nguồn liên quan:**
  - `TAI_LIEU_KHAO_SAT.md` (Tạo mới)
  - `DE_CUONG_DO_AN.md` (Tạo mới)
  - `.gitignore` (Tạo mới)
  - `README.md` (Tạo mới)
  - `data/schemas/.gitkeep`, `data/generated/.gitkeep`, `benchmarks/queries/.gitkeep`, `results/data/.gitkeep`, `results/charts/.gitkeep` (Tạo mới)
- **Bước tiếp theo cần làm:** Bắt đầu triển khai Giai đoạn 2 theo chỉ đạo của người dùng.

### [2026-09-16 12:55] - Hoàn Thành Giai Đoạn 2: Thiết Kế Mô Hình Dữ Liệu Đồng Nhất (Task 2.1 - 2.5)
- **Trạng thái:** ✅ Hoàn thành
- **Công việc đã thực hiện:**
  - **Task 2.1:** Thống nhất miền nghiệp vụ Mạng xã hội theo các quyết định của người dùng: Quan hệ Follows có hướng (1 chiều), Comments nhúng trong Posts ở MongoDB, và Tags là thực thể độc lập.
  - **Task 2.2:** Thiết kế lược đồ CSDL Quan hệ PostgreSQL chuẩn hóa 3NF (`users`, `follows`, `posts`, `comments`, `tags`, `post_tags`) và xuất mã nguồn DDL vào `data/schemas/postgresql_schema.sql`.
  - **Task 2.3:** Thiết kế lược đồ CSDL Tài liệu MongoDB với JSON Schema Validator, nhúng bình luận và mảng tags, xuất mã nguồn vào `data/schemas/mongodb_schema.js`.
  - **Task 2.4:** Thiết kế lược đồ CSDL Đồ thị Neo4j với Uniqueness Constraints và Schema Indexes, xuất mã nguồn Cypher vào `data/schemas/neo4j_schema.cypher`.
  - **Task 2.5:** Thiết lập chiến lược đánh chỉ mục đồng bộ, công bằng cho cả 3 CSDL (B-Tree trên Postgres, Compound & Multikey trên Mongo, Schema Index trên Neo4j).
  - Soạn thảo tài liệu đặc tả kiến trúc tổng thể, biểu đồ UML Use Case, ERD, Document Diagram, Graph Diagram và Ma trận truy vết trong `THIET_KE_CSDL_VA_USECASE.md`.
  - Cập nhật tiến độ trong `TODO.md` đạt **9/37 tasks (24.3%)**.
- **Tài liệu / Mã nguồn liên quan:**
  - `THIET_KE_CSDL_VA_USECASE.md` (Tạo mới)
  - `data/schemas/postgresql_schema.sql` (Tạo mới)
  - `data/schemas/mongodb_schema.js` (Tạo mới)
  - `data/schemas/neo4j_schema.cypher` (Tạo mới)
  - `TODO.md` (Cập nhật 5 task hoàn thành)
- **Bước tiếp theo cần làm:** Bắt đầu thực hiện Giai đoạn 3 (Xây dựng hạ tầng Cloud "Một Thao Tác" với Docker Compose và Dev Containers trên Codespaces).

### [2026-09-16 13:15] - Đổi Tên Thư Mục Gốc Dự Án Sang 'cloud-db-benchmark'
- **Trạng thái:** ✅ Hoàn thành
- **Công việc đã thực hiện:**
  - Đổi tên thư mục gốc từ `C:\Users\ADMIN\Desktop\Do_an` thành `C:\Users\ADMIN\Desktop\cloud-db-benchmark` để đồng bộ chuẩn hóa 100% với tên GitHub Repository.
  - Cập nhật toàn bộ các đường dẫn tham chiếu trong `TODO.md`, `PROGRESS.md`, `README.md`, `explain.md`, và `THIET_KE_CSDL_VA_USECASE.md`.
- **Tài liệu / Mã nguồn liên quan:**
  - Thư mục dự án: `C:\Users\ADMIN\Desktop\cloud-db-benchmark`
- **Bước tiếp theo cần làm:** Sẵn sàng kết nối và đẩy code lên GitHub repository `cloud-db-benchmark`.
