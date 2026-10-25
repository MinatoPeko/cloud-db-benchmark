# BÁO CÁO KIỂM THỬ XÁC MINH HỆ THỐNG BENCHMARK (QA VERIFICATION REPORT)

- **Dự án:** Nghiên cứu, đánh giá hiệu năng các mô hình CSDL (PostgreSQL, MongoDB, Neo4j) trên môi trường ảo hóa Dev Container
- **Quy mô xác minh:** `TEST` (100 users, 500 follows, 151 posts, 247 comments, 30 tags)
- **Số vòng lặp (Iterations):** 5 rounds / use case
- **Thời gian thực hiện:** 24/10/2026
- **Trạng thái tổng thể:** ✅ **PASSED (100% HOÀN TẤT & KHỚP DỮ LIỆU)**

---

## 1. Lưu trữ Dữ liệu & Hiện vật (Artifacts & Data Persistence)

Tất cả các thông số đo kiểm, log dữ liệu và biểu đồ đã được lưu trữ vĩnh viễn tại các đường dẫn sau:

1. **File số liệu thô (Raw CSV Benchmark Data):**  
   - `results/data/results_test_20261024_221659.csv` (21 bản ghi chi tiết với 18 trường thông số)
2. **File biểu đồ trực quan hóa độ phân giải cao 300 DPI:**  
   - `results/charts/01_latency_bar_test_20261024_221659.png` (So sánh Mean Latency)
   - `results/charts/02_p99_heatmap_test_20261024_221659.png` (Heatmap p99 Latency)
   - `results/charts/03_qps_bar_test_20261024_221659.png` (So sánh Thông lượng QPS)
   - `results/charts/04_ram_bar_test_20261024_221659.png` (Mức tiêu thụ RAM trung bình)

---

## 2. Bước 1 - Kiểm tra kết nối CSDL (Healthcheck)

- **Lệnh thực thi:** `python benchmarks/healthcheck.py`
- **Kết quả:**
  - **PostgreSQL 16.15**: ✅ Sẵn sàng (`latency: 152.3 ms`)
  - **MongoDB 7.0.45**: ✅ Sẵn sàng (`latency: 52.9 ms`)
  - **Neo4j 5.26.32**: ✅ Sẵn sàng (`latency: 5949.1 ms` - Bolt Protocol)

---

## 3. Bước 2 - Nạp dữ liệu và kiểm tra toàn vẹn (Data Integrity & Checksum)

- **Lệnh thực thi:**
  - `python data/import_all.py --scale test` (Thời gian nạp hoàn tất: **16.98 giây**)
  - `python data/verify_data.py`

### Bảng đối soát số lượng thực thể (Data Checksum Verification Table)

| Thực thể | PostgreSQL | MongoDB | Neo4j | Trạng thái đối soát |
| :--- | :---: | :---: | :---: | :---: |
| **users** | 100 | 100 | 100 | ✅ Khớp 100% |
| **follows** | 500 | 500 | 500 | ✅ Khớp 100% |
| **posts** | 151 | 151 | 151 | ✅ Khớp 100% |
| **comments** | 247 | 247 | 247 | ✅ Khớp 100% |
| **tags** | 30 | 30 | 30 | ✅ Khớp 100% |

**Kết luận toàn vẹn:** Khớp 100% trên toàn bộ 5 thực thể. Không thất thoát hoặc sai lệch dữ liệu giữa 3 mô hình CSDL.

---

## 4. Bước 3 - Kết quả đo kiểm Hiệu năng (Latency, QPS, CPU, RAM)

- **Lệnh thực thi:** `python benchmarks/runner.py --scale test --iterations 5`

| CSDL | Mã UC | Tên Use Case | Mean (ms) | p50 (ms) | p95 (ms) | p99 (ms) | QPS | CPU TB (%) | RAM Đỉnh (MB) | Disk Read (MB) | Disk Write (MB) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **PostgreSQL** | UC-01 | Single Insert | 4.21 | 1.48 | 15.31 | 15.31 | 237.3 | 0.0% | 10,768.1 | 1.75 | 0.17 |
| | UC-02 | Point Read | 2.45 | 1.66 | 6.13 | 6.13 | 407.5 | 0.0% | 10,772.2 | 0.74 | 0.10 |
| | UC-03 | Join Read | 3.89 | 2.25 | 9.73 | 9.73 | 257.3 | 0.0% | 10,747.3 | 1.71 | 0.60 |
| | UC-04 | Aggregation | 4.75 | 2.56 | 14.26 | 14.26 | 210.4 | 0.0% | 10,773.6 | 0.32 | 0.09 |
| | UC-05 | 1-hop Traversal | 2.01 | 1.45 | 4.26 | 4.26 | 497.8 | 0.0% | 10,776.3 | 2.11 | 0.04 |
| | UC-06 | 2-hop FOAF | 3.86 | 3.41 | 6.72 | 6.72 | 259.1 | 0.0% | 10,764.1 | 1.14 | 0.15 |
| | UC-07 | Shortest Path | 10.90 | 4.26 | 37.76 | 37.76 | 91.7 | 0.0% | 10,753.4 | 3.63 | 0.03 |
| **MongoDB** | UC-01 | Single Insert | 12.17 | 2.95 | 43.43 | 43.43 | 82.2 | 0.0% | 10,779.8 | 4.01 | 0.10 |
| | UC-02 | Point Read | 4.45 | 3.82 | 8.15 | 8.15 | 224.5 | 0.0% | 10,795.5 | 1.57 | 0.00 |
| | UC-03 | Embedded Read | 6.42 | 6.60 | 9.77 | 9.77 | 155.7 | 0.0% | 10,823.9 | 2.30 | 0.24 |
| | UC-04 | Aggregation | 13.93 | 5.05 | 46.85 | 46.85 | 71.8 | 0.0% | 10,816.5 | 1.61 | 0.14 |
| | UC-05 | 1-hop Traversal | 6.23 | 5.83 | 12.61 | 12.61 | 160.5 | 0.0% | 10,856.6 | 2.10 | 1.64 |
| | UC-06 | 2-hop FOAF | 8.55 | 5.88 | 19.82 | 19.82 | 117.0 | 0.0% | 10,852.2 | 1.58 | 0.13 |
| | UC-07 | Shortest Path | 15.04 | 9.04 | 41.31 | 41.31 | 66.5 | 0.0% | 10,863.0 | 2.44 | 0.11 |
| **Neo4j** | UC-01 | Single Insert | 111.63 | 33.84 | 418.31 | 418.31 | 9.0 | 38.5% | 10,889.0 | 3.79 | 2.98 |
| | UC-02 | Point Read | 66.10 | 13.21 | 218.57 | 218.57 | 15.1 | 0.0% | 10,884.5 | 0.36 | 0.10 |
| | UC-03 | Join Read | 113.75 | 19.86 | 494.08 | 494.08 | 8.8 | 64.7% | 10,896.6 | 3.61 | 0.62 |
| | UC-04 | Aggregation | 168.73 | 53.37 | 638.14 | 638.14 | 5.9 | 49.7% | 10,950.1 | 3.41 | 0.08 |
| | UC-05 | 1-hop Traversal | 79.53 | 21.95 | 314.16 | 314.16 | 12.6 | 0.0% | 10,954.6 | 2.25 | 0.52 |
| | UC-06 | 2-hop FOAF | 217.27 | 18.03 | 1016.79 | 1016.79 | 4.6 | 63.1% | 10,984.1 | 12.98 | 1.68 |
| | UC-07 | Shortest Path | 82.91 | 14.22 | 357.35 | 357.35 | 12.1 | 0.0% | 10,959.7 | 3.66 | 0.03 |

---

## 5. Bước 4 - Tạo biểu đồ trực quan (Visualization)

- **Lệnh thực thi:** `python results/visualize.py`
- **Kết quả:** Đã đọc tự động file kết quả mới nhất và vẽ 4 biểu đồ lưu vào thư mục `results/charts/`.

---

## 6. Ghi nhận lỗi đã sửa (Bug Fixes)

1. **`benchmarks/runner.py`**: Bổ sung cờ `--iterations` song song với `--rounds` để tương thích quy chuẩn QA.
2. **`benchmarks/runner.py`**: Sửa cấu trúc import `from monitor import ResourceMonitor` để cho phép chạy script trực tiếp từ dòng lệnh.
