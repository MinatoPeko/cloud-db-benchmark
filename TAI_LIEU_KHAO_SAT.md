# 📚 TỔNG QUAN TÀI LIỆU NGHIÊN CỨU & CƠ SỞ KHOA HỌC (LITERATURE REVIEW)

> **Đề tài:** Nghiên cứu, đánh giá hiệu năng các mô hình cơ sở dữ liệu quan hệ, phi quan hệ và đồ thị trên môi trường phát triển ảo hóa Cloud-based (GitHub Codespaces)  
> **Ngành:** Kỹ thuật Phần mềm - Trường Đại học Phenikaa  
> **Mã task:** Task 1.1 (TODO.md)  
> **Mục đích:** Cung cấp cơ sở học thuật, các công trình nghiên cứu tiền đề chuẩn IEEE/ACM để đưa trực tiếp vào **Chương 1 (Tổng quan)** và **Chương 2 (Cơ sở lý thuyết)** của Báo cáo Đồ án.

---

## 1. CÁC CÔNG TRÌNH NGHIÊN CỨU TIỀN ĐỀ QUỐC TẾ

Dưới đây là các công trình nghiên cứu khoa học tiêu biểu đã được bình duyệt (peer-reviewed) trên các tạp chí và hội nghị uy tín về việc so sánh hiệu năng giữa CSDL Quan hệ (RDBMS), Phi quan hệ (Document NoSQL) và Đồ thị (Graph DB):

### 1.1. So sánh CSDL Đồ thị (Neo4j) và CSDL Quan hệ (RDBMS)
- **Tài liệu 1:** *Vicknair, C., Macias, M., Zhao, Z., Nan, X., Chen, Y., & Wilkins, D. (2010). "A comparison of a graph database and a relational database: a data provenance perspective." Proceedings of the 48th Annual Southeast Regional Conference (ACM SE '10).*
  - **Phát hiện chính:** Khi độ sâu truy vấn tăng (quan hệ từ 2-hop trở lên), CSDL quan hệ (MySQL) bị suy giảm hiệu năng nghiêm trọng do chi phí nối bảng (`JOIN`) tăng theo cấp số nhân, trong khi Neo4j duy trì thời gian đáp ứng ổn định nhờ con trỏ trực tiếp giữa các nút (Index-free Adjacency).
  - **Áp dụng cho đồ án:** Sử dụng kết luận này làm giả thuyết nghiên cứu cho Kịch bản đo kiểm Graph Multi-hop (1-hop đến 4-hop).

- **Tài liệu 2:** *Batra, C., & Tyagi, C. (2012). "Comparative Analysis of Relational and Graph Databases." International Journal of Computer Applications, 43(20), 9-12.*
  - **Phát hiện chính:** Phân tích sự khác biệt về cấu trúc lưu trữ. Với các dữ liệu có mức độ liên kết cao (Highly-connected data), mô hình đồ thị giảm thiểu số lượng phép quét đĩa (Disk I/O) so với mô hình bảng chuẩn hóa (3NF) của RDBMS.

- **Tài liệu 3:** *Holzschuher, F., & Peinl, R. (2013). "Performance of graph query languages: comparison of Cypher, Gremlin and native access in Neo4j." Proceedings of the Joint EDBT/ICDT 2013 Workshops (ACM).*
  - **Phát hiện chính:** Đánh giá chi phí overhead của ngôn ngữ truy vấn Cypher và khuyến nghị các kỹ thuật lập chỉ mục (Schema Index) trên Neo4j để tối ưu truy vấn tìm nút bắt đầu.

### 1.2. So sánh CSDL Hướng tài liệu (MongoDB) và CSDL Quan hệ (PostgreSQL / MySQL)
- **Tài liệu 4:** *Li, Y., & Manoharan, S. (2013). "A performance comparison of SQL and NoSQL databases." IEEE 2013 Pacific Rim Conference on Communications, Computers and Signal Processing (PACRIM).*
  - **Phát hiện chính:** MongoDB vượt trội hơn hẳn các hệ CSDL quan hệ ở thao tác ghi hàng loạt (Bulk Insert) và đọc dữ liệu không cấu trúc nhờ cơ chế nhúng (Embedding) không cần ràng buộc toàn vẹn khóa ngoại.
  - **Áp dụng cho đồ án:** Sử dụng làm cơ sở đối chiếu cho Kịch bản CRUD đơn lẻ và Batch Insert.

- **Tài liệu 5:** *Győrödi, C., Győrödi, R., Pecherle, G., & Olah, A. (2015). "A comparative study: MongoDB vs. MySQL." IEEE 13th International Conference on Engineering of Modern Electric Systems (EMES).*
  - **Phát hiện chính:** Với các truy vấn đọc đơn giản trên tập dữ liệu lớn, MongoDB có thời gian phản hồi nhanh hơn, nhưng khi thực hiện các phép lọc phức tạp nhiều điều kiện, RDBMS với B-Tree index lại có độ ổn định tài nguyên tốt hơn.

### 1.3. Xu hướng Benchmarking CSDL trên môi trường Cloud & Container
- **Tài liệu 6:** *Angles, R., Arenas, M., Barceló, P., Hogan, A., Reutter, J., & Vrgoč, D. (2020). "Benchmarking Graph Databases: Past, Present and Future." GraphQ '20 (ACM).*
  - **Phát hiện chính:** Chỉ ra sự thiếu chuẩn hóa trong việc thiết lập môi trường đo kiểm CSDL giữa các nghiên cứu độc lập. Đề xuất việc chuẩn hóa môi trường thực nghiệm bằng container hóa để đảm bảo tính tái lập (Reproducibility).
  - **Ý nghĩa với đề tài:** Khẳng định tính cấp thiết và tính thời sự của việc sử dụng **GitHub Codespaces (Dev Containers)** trong đồ án của bạn!

---

## 2. BẢNG TỔNG HỢP MA TRẬN ĐẶC TÍNH KỸ THUẬT (THEO Y KHOA / KHOA HỌC MÁY TÍNH)

| Tiêu chí | **PostgreSQL 16 (Relational)** | **MongoDB 7.0 (Document)** | **Neo4j 5.x (Property Graph)** |
| :--- | :--- | :--- | :--- |
| **Mô hình cốt lõi** | Quan hệ (Bảng 2 chiều, Khóa chính, Khóa ngoại) | Tài liệu BSON (Cây phân cấp, nhúng / tham chiếu) | Đồ thị thuộc tính (Nút, Cạnh, Nhãn, Thuộc tính) |
| **Cơ chế lưu trữ** | Heap File + Shared Buffers | WiredTiger Engine (B-Tree + Cache) | Record-based Storage (Nodes, Relationships, Properties riêng biệt) |
| **Cơ chế liên kết** | Ghép bảng thời điểm truy vấn (`Hash Join`, `Merge Join`, `Nested Loop`) | Nhúng tài liệu hoặc `$lookup` / `$graphLookup` | **Index-free Adjacency** (Con trỏ bộ nhớ hai chiều trực tiếp) |
| **Độ phức tạp truy vấn n-hop** | Tăng theo hàm số mũ $O(k^n)$ | Tăng nhanh theo độ sâu đệ quy | Tuyến tính theo số cạnh cục bộ $O(k)$ |
| **Mức độ toàn vẹn** | Chuẩn ACID nghiêm ngặt | ACID mức Document (hỗ trợ Multi-doc Transaction) | Chuẩn ACID đầy đủ cho đồ thị |
| **Phù hợp nhất với** | Dữ liệu giao dịch, tài chính, quan hệ có cấu trúc cố định | Nội dung web, catalog sản phẩm, dữ liệu JSON linh hoạt | Mạng xã hội, hệ thống gợi ý, phát hiện gian lận, tri thức |

---

## 3. KHOẢNG TRỐNG NGHIÊN CỨU & ĐÓNG GÓP MỚI CỦA ĐỒ ÁN (RESEARCH GAP)

Mặc dù đã có nhiều công trình so sánh riêng rẽ từng cặp (SQL vs NoSQL hoặc SQL vs Graph), nhưng hầu hết đều gặp phải các hạn chế sau:
1. **Thiếu tính đồng nhất môi trường:** Đa số các thử nghiệm cũ chạy trên máy trạm cục bộ (Bare-metal / Local PC) với nhiều tiến trình nền gây nhiễu, không thể chia sẻ môi trường cho người khác chạy lại kiểm chứng.
2. **Chưa so sánh đồng thời cả 3 mô hình trên cùng một bài toán:** Rất ít công trình đặt cả 3 họ CSDL đại diện vào cùng một tập dữ liệu nghiệp vụ duy nhất (Mạng xã hội) với đầy đủ các mức quy mô dữ liệu.
3. **Đóng góp mới của đồ án này:**
   - Xây dựng một quy trình thử nghiệm **chuẩn hóa 100% trên Cloud (GitHub Codespaces)**: Đóng gói toàn bộ mã nguồn, cấu hình hạ tầng (Infrastructure as Code) và bộ dữ liệu vào một Dev Container.
   - Bất kỳ nhà nghiên cứu nào trên thế giới chỉ cần 1 click là có thể tái lập chính xác toàn bộ kết quả đo đạc.
   - Cung cấp một **Ma trận quyết định (Decision Matrix)** thực tế cho các kỹ sư phần mềm khi lựa chọn kiến trúc lưu trữ dữ liệu đám mây.
