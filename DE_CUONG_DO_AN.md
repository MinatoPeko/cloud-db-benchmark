# TRƯỜNG ĐẠI HỌC PHENIKAA
## KHOA CÔNG NGHỆ THÔNG TIN - BỘ MÔN KỸ THUẬT PHẦN MỀM
***

# ĐỀ CƯƠNG CHI TIẾT ĐỒ ÁN CHUYÊN NGÀNH

- **Tên đề tài:** Nghiên cứu, đánh giá hiệu năng các mô hình cơ sở dữ liệu quan hệ, phi quan hệ và đồ thị trên môi trường phát triển ảo hóa Cloud-based (GitHub Codespaces)
- **Sinh viên thực hiện:** `[Họ và tên sinh viên]`
- **Mã sinh viên:** `[Mã sinh viên]`
- **Lớp:** `[Lớp]`
- **Ngành đào tạo:** Kỹ thuật Phần mềm
- **Khóa:** `[Khóa]`
- **Giảng viên hướng dẫn:** `[TS/ThS. Giảng viên hướng dẫn]`
- **Thời gian thực hiện:** 10 tuần (Học kỳ I, Năm học 2026 - 2027)

---

## 1. TÍNH CẤP THIẾT CỦA ĐỀ TÀI (RATIONALE)

Trong kỷ nguyên điện toán đám mây (Cloud Computing) và dữ liệu lớn (Big Data), việc lựa chọn kiến trúc lưu trữ dữ liệu phù hợp đóng vai trò sống còn đối với hiệu năng, khả năng mở rộng và chi phí vận hành của các hệ thống phần mềm hiện đại. Kỹ sư phần mềm ngày nay đứng trước nhiều lựa chọn đa dạng: từ CSDL quan hệ truyền thống (Relational - RDBMS), CSDL hướng tài liệu (Document NoSQL), cho đến CSDL đồ thị (Graph Database).

Tuy nhiên, việc lựa chọn CSDL trong thực tế thường mang tính cảm tính hoặc phụ thuộc vào thói quen công nghệ, thiếu các căn cứ định lượng khoa học. Hơn nữa, việc đo kiểm hiệu năng CSDL trên các máy tính cục bộ (local bare-metal) thường gặp phải vấn đề thiếu khách quan do khác biệt phần cứng và không thể tái lập (lack of reproducibility).

Sự xuất hiện của các môi trường phát triển ảo hóa trên đám mây (Cloud-based Development Environments như **GitHub Codespaces**) kết hợp với công nghệ container hóa (**Dev Containers / Docker**) mở ra giải pháp lý tưởng: cho phép chuẩn hóa cấu hình phần cứng, tự động hóa môi trường thử nghiệm và đảm bảo tính tái lập 100% cho bất kỳ ai muốn kiểm chứng kết quả.

Xuất phát từ bối cảnh đó, đề tài **"Nghiên cứu, đánh giá hiệu năng các mô hình cơ sở dữ liệu quan hệ, phi quan hệ và đồ thị trên môi trường phát triển ảo hóa Cloud-based (GitHub Codespaces)"** được đề xuất nhằm cung cấp một khung thực nghiệm chuẩn mực và ma trận khuyến nghị thực tiễn cho kỹ sư phần mềm.

---

## 2. MỤC TIÊU VÀ PHẠM VI NGHIÊN CỨU

### 2.1. Mục tiêu chung
Xây dựng một hệ thống thử nghiệm tự động hóa trên GitHub Codespaces để đo lường, so sánh định lượng hiệu năng của 3 mô hình CSDL đại diện, từ đó xây dựng ma trận khuyến nghị lựa chọn CSDL cho từng bài toán kỹ thuật phần mềm cụ thể.

### 2.2. Mục tiêu cụ thể
1. **Lý thuyết:** Phân tích sâu kiến trúc động cơ lưu trữ (Storage Engines), cơ chế lập chỉ mục (Indexing) và thuật toán thực thi truy vấn của:
   - CSDL Quan hệ: **PostgreSQL 16** (B-Tree, relational algebra, SQL Joins).
   - CSDL Phi quan hệ: **MongoDB 7.0** (WiredTiger, BSON, nested documents, Aggregation).
   - CSDL Đồ thị: **Neo4j 5.x** (Property Graph Model, Index-free Adjacency, Cypher).
2. **Hạ tầng (Cloud IaC):** Xây dựng cấu hình hạ tầng hoàn chỉnh (`.devcontainer` + `docker-compose.yml`) cho phép khởi tạo đồng thời 3 hệ CSDL trên GitHub Codespaces chỉ với **một thao tác (One-click setup)**.
3. **Thực nghiệm & Đo lường:** Thiết kế bộ dữ liệu mẫu thực tế (Mạng xã hội ảo) với 3 quy mô (Small 10K, Medium 100K, Large 500K records) và thực thi 4 nhóm kịch bản đo kiểm:
   - Kịch bản CRUD & Bulk Write.
   - Kịch bản Lọc & Tổng hợp dữ liệu (Aggregation & Filtering).
   - Kịch bản Truy vấn quan hệ đa tầng (Graph Traversals từ 1-hop đến 4-hop).
   - Kịch bản Giám sát tiêu hao tài nguyên ảo hóa (CPU %, RAM MB, Disk I/O).
4. **Đóng góp ứng dụng:** Xây dựng **Ma trận Quyết định (Decision Matrix)** hỗ trợ kỹ sư phần mềm đưa ra quyết định kiến trúc chính xác.

### 2.3. Phạm vi nghiên cứu
- **Hạ tầng phần cứng Cloud cố định:** GitHub Codespaces máy ảo cấu hình tiêu chuẩn dành cho sinh viên (**4 vCPUs, 16 GB RAM, 32 GB SSD Storage**, hệ điều hành Linux/Ubuntu container).
- **Hệ quản trị CSDL thử nghiệm:** PostgreSQL 16-alpine, MongoDB 7.0, Neo4j 5.x-community.
- **Tập dữ liệu nghiệp vụ:** Miền bài toán Mạng xã hội & Tương tác (Users, Friendships, Posts, Comments, Tags).

---

## 3. ĐỐI TƯỢNG VÀ PHƯƠNG PHÁP NGHIÊN CỨU

### 3.1. Đối tượng nghiên cứu
- Các mô hình tổ chức dữ liệu: Quan hệ (Bảng 2 chiều), Phi quan hệ (Tài liệu BSON), và Đồ thị (Đỉnh/Cạnh thuộc tính).
- Các chỉ số đánh giá hiệu năng phần mềm:
  - Thời gian phản hồi (Latency: Mean, p50, p95, p99 theo mili-giây).
  - Thông lượng xử lý (Throughput / QPS: Số truy vấn hoàn thành trên giây).
  - Mức độ tiêu thụ tài nguyên máy ảo (CPU Usage %, RAM Allocation MB).
- Môi trường ảo hóa đám mây GitHub Codespaces và cơ chế Dev Containers.

### 3.2. Phương pháp nghiên cứu
1. **Phương pháp nghiên cứu lý thuyết:** Thu thập, phân tích và tổng hợp các công trình nghiên cứu khoa học uy tín (IEEE, ACM) về so sánh CSDL và tối ưu hóa truy vấn.
2. **Phương pháp mô hình hóa kỹ thuật phần mềm:** Áp dụng chuẩn UML (Use Case Diagram, Deployment Diagram, ERD/Schema Diagram) để thiết kế hệ thống và bài toán dữ liệu.
3. **Phương pháp thực nghiệm định lượng (Empirical Benchmark):**
   - Viết công cụ đo đạc tự động bằng Python (`asyncio`, `psutil`, database native drivers).
   - Áp dụng kỹ thuật kiểm soát bộ đệm (Warm-up cache & Cold cache runs).
   - Mỗi kịch bản được lặp lại 5–10 lần, tính trung bình và độ lệch chuẩn để đảm bảo độ tin cậy thống kê.
4. **Phương pháp so sánh và tổng hợp:** Sử dụng biểu đồ trực quan (Matplotlib/Seaborn) và phân tích kế hoạch thực thi câu lệnh (`EXPLAIN ANALYZE`, `.explain()`, `PROFILE`) để giải thích nguyên nhân gốc rễ.

---

## 4. KẾ HOẠCH VÀ TIẾN ĐỘ THỰC HIỆN (10 TUẦN)

| Tuần | Nội dung công việc | Sản phẩm / Kết quả đạt được |
| :---: | :--- | :--- |
| **Tuần 1** | Khảo sát tài liệu khoa học, hoàn thiện đề cương chi tiết nộp GVHD ký duyệt. Khởi tạo repository GitHub. | Bản Đề cương chi tiết, Repo GitHub, file `TAI_LIEU_KHAO_SAT.md`. |
| **Tuần 2** | Thiết lập hạ tầng ảo hóa Cloud: Viết `.devcontainer` và `docker-compose.yml` trên GitHub Codespaces. | Môi trường 3 CSDL chạy hoàn hảo với 1-click mở Codespace. |
| **Tuần 3** | Thiết kế nghiệp vụ, Use Case và mô hình dữ liệu đồng nhất (PostgreSQL ERD, MongoDB Schema, Neo4j Graph). | Tài liệu thiết kế CSDL và đặc tả Use Case chuẩn UML. |
| **Tuần 4** | Viết script sinh dữ liệu giả lập (`datagen.py`) và pipeline nạp dữ liệu tự động cho 3 quy mô (Small, Medium, Large). | Dữ liệu 10K, 100K, 500K records được nạp toàn vẹn vào 3 CSDL. |
| **Tuần 5** | Phát triển bộ công cụ Benchmark Harness (`benchmark_runner.py`) đo Latency, QPS, CPU, RAM. | Tool benchmark tự động hóa, kiểm soát warm/cold cache. |
| **Tuần 6** | Thực nghiệm đợt 1: Đo kiểm Kịch bản CRUD đơn lẻ, Bulk Write và Aggregation/Filtering. | Tập dữ liệu thô (raw JSON/CSV) kết quả đợt 1. |
| **Tuần 7** | Thực nghiệm đợt 2: Đo kiểm Kịch bản Graph Traversals (1-hop đến 4-hop) và tiêu hao tài nguyên. | Tập dữ liệu thô kết quả đợt 2, chụp Query Execution Plans. |
| **Tuần 8** | Phân tích số liệu, trực quan hóa biểu đồ khoa học và xây dựng Ma trận Quyết định (Decision Matrix). | Bộ biểu đồ chất lượng cao (300 DPI) và bản thảo Ma trận khuyến nghị. |
| **Tuần 9** | Soạn thảo toàn văn Báo cáo Đồ án Chuyên ngành (5 chương) theo quy chuẩn Đại học Phenikaa. | Bản thảo Báo cáo Đồ án hoàn chỉnh gửi GVHD xin nhận xét. |
| **Tuần 10** | Chỉnh sửa báo cáo theo góp ý của GVHD, đóng gói mã nguồn, thiết kế Slide và kịch bản Live Demo. | Cuốn Báo cáo hoàn thiện, Slide thuyết trình, Video/Demo kịch bản. |

---

## 5. KẾT QUẢ DỰ KIẾN VÀ SẢN PHẨM BÀN GIAO

1. **Bộ mã nguồn dự án hoàn chỉnh (GitHub Repository):**
   - Cấu hình hạ tầng Dev Container sẵn sàng chạy trên GitHub Codespaces chỉ với 1-click.
   - Script sinh dữ liệu thực tế và pipeline nạp dữ liệu tự động.
   - Bộ công cụ đo kiểm benchmark tự động hóa bằng Python.
   - Script trực quan hóa biểu đồ kết quả (`visualize.py`).
2. **Cuốn Báo cáo Đồ án Chuyên ngành:**
   - Soạn thảo đúng quy định hình thức của Trường Đại học Phenikaa (khoảng 60–80 trang).
   - Cấu trúc 5 chương hoàn chỉnh: Mở đầu, Cơ sở lý thuyết, Thiết kế thực nghiệm, Kết quả & Đánh giá, Kết luận & Khuyến nghị.
3. **Ma trận Quyết định Lựa chọn CSDL:**
   - Cẩm nang so sánh đa chiều cung cấp căn cứ kỹ thuật cho các kỹ sư phần mềm khi thiết kế kiến trúc hệ thống.
4. **Slide thuyết trình & Kịch bản Live Demo:**
   - Slide báo cáo trước Hội đồng (15–20 slides súc tích).
   - Kịch bản demo thực tế chạy trực tiếp trên Codespaces trước Hội đồng bảo vệ.

---

## 6. TÀI LIỆU THAM KHẢO CHÍNH

1. Vicknair, C., et al. (2010). *"A comparison of a graph database and a relational database: a data provenance perspective."* ACM SE '10.
2. Batra, C., & Tyagi, C. (2012). *"Comparative Analysis of Relational and Graph Databases."* IJCA, 43(20), 9-12.
3. Li, Y., & Manoharan, S. (2013). *"A performance comparison of SQL and NoSQL databases."* IEEE PACRIM.
4. Győrödi, C., et al. (2015). *"A comparative study: MongoDB vs. MySQL."* IEEE EMES.
5. Angles, R., et al. (2020). *"Benchmarking Graph Databases: Past, Present and Future."* ACM GraphQ '20.
6. GitHub Docs. (2024). *"Developing in a Codespace & Dev Containers Specification."*

---

| GIẢNG VIÊN HƯỚNG DẪN DUYỆT | SINH VIÊN THỰC HIỆN |
| :---: | :---: |
| *(Ký và ghi rõ họ tên)* | *(Ký và ghi rõ họ tên)* |
| <br><br><br> | <br><br><br> |
| **`[TS/ThS. Giảng viên hướng dẫn]`** | **`[Họ và tên sinh viên]`** |
