# BÁO CÁO KẾT QUẢ BENCHMARK CHÍNH THỨC - QUY MÔ SMALL (10.000 USERS)

- **Môi trường:** Dev Container ảo hóa (PostgreSQL 16, MongoDB 7.0, Neo4j 5.x)
- **Quy mô dữ liệu (SMALL):**
  - Users: 10,000
  - Follows: 50,000
  - Posts: 24,994
  - Comments: 63,115
  - Tags: 30
- **Số vòng đo lặp (Iterations):** 20 rounds / Use Case (loại trừ cold start, đo p50, p95, p99)
- **Thời gian thực thi:** 24/10/2026
- **Trạng thái đối soát dữ liệu (Checksum):** ✅ **Khớp 100% trên cả 5 thực thể**

---

## 1. Lưu trữ Tài liệu & Dữ liệu Nghiên cứu

- **File dữ liệu thô CSV (21 dòng x 18 cột):**  
  `results/data/results_small_20261024_233530.csv`
- **File biểu đồ phân tích 300 DPI:**  
  - `results/charts/01_latency_bar_small_20261024_233530.png`
  - `results/charts/02_p99_heatmap_small_20261024_233530.png`
  - `results/charts/03_qps_bar_small_20261024_233530.png`
  - `results/charts/04_ram_bar_small_20261024_233530.png`

---

## 2. Bảng Đối soát Toàn vẹn Dữ liệu (Data Checksum)

| Thực thể | PostgreSQL | MongoDB | Neo4j | Kết quả kiểm tra |
| :--- | :---: | :---: | :---: | :---: |
| **users** | 10,000 | 10,000 | 10,000 | ✅ Khớp 100% |
| **follows** | 50,000 | 50,000 | 50,000 | ✅ Khớp 100% |
| **posts** | 24,994 | 24,994 | 24,994 | ✅ Khớp 100% |
| **comments** | 63,115 | 63,115 | 63,115 | ✅ Khớp 100% |
| **tags** | 30 | 30 | 30 | ✅ Khớp 100% |

---

## 3. Bảng Tổng hợp Hiệu năng Chi tiết (20 Vòng lặp)

| CSDL | Mã UC | Tên Use Case | Mean (ms) | p50 (ms) | p95 (ms) | p99 (ms) | QPS | CPU TB (%) | RAM Đỉnh (MB) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **PostgreSQL** | UC-01 | Single Insert | 5.43 | 1.92 | 73.53 | 73.53 | 184.0 | 0.0% | 11,574.8 |
| | UC-02 | Point Read | 2.67 | 1.96 | 15.83 | 15.83 | 374.3 | 50.0% | 11,566.1 |
| | UC-03 | Join Read | 3.28 | 2.13 | 23.94 | 23.94 | 304.7 | 0.0% | 11,577.4 |
| | UC-04 | Aggregation | 55.01 | 47.04 | 200.51 | 200.51 | 18.2 | 64.4% | 11,603.5 |
| | UC-05 | 1-hop Traversal | 2.17 | 1.98 | 6.29 | 6.29 | 459.9 | 0.0% | 11,584.6 |
| | UC-06 | 2-hop FOAF | 6.30 | 3.96 | 28.96 | 28.96 | 158.6 | 0.0% | 11,500.9 |
| | UC-07 | Shortest Path | 7.07 | 5.65 | 33.46 | 33.46 | 141.5 | 0.0% | 11,247.2 |
| **MongoDB** | UC-01 | Single Insert | 5.22 | 2.98 | 40.66 | 40.66 | 191.7 | 0.0% | 11,307.7 |
| | UC-02 | Point Read | 2.90 | 2.61 | 8.82 | 8.82 | 345.3 | 0.0% | 11,292.9 |
| | UC-03 | Embedded Read | 3.44 | 3.08 | 5.77 | 5.77 | 290.5 | 0.0% | 11,294.0 |
| | UC-04 | Aggregation | 65.46 | 60.67 | 186.67 | 186.67 | 15.3 | 38.3% | 11,214.2 |
| | UC-05 | 1-hop Traversal | 3.07 | 2.54 | 13.46 | 13.46 | 326.2 | 0.0% | 11,198.0 |
| | UC-06 | 2-hop FOAF | 6.86 | 6.56 | 16.44 | 16.44 | 145.8 | 0.0% | 11,208.6 |
| | UC-07 | Shortest Path | 15.58 | 15.27 | 23.40 | 23.40 | 64.2 | 0.0% | 11,211.4 |
| **Neo4j** | UC-01 | Single Insert | 63.47 | 21.01 | 863.80 | 863.80 | 15.8 | 47.6% | 11,363.4 |
| | UC-02 | Point Read | 44.43 | 39.11 | 286.03 | 286.03 | 22.5 | 48.0% | 11,424.2 |
| | UC-03 | Join Read | 66.18 | 46.91 | 433.19 | 433.19 | 15.1 | 53.7% | 11,454.3 |
| | UC-04 | Aggregation | 128.00 | 102.15 | 579.54 | 579.54 | 7.8 | 73.5% | 11,522.0 |
| | UC-05 | 1-hop Traversal | 33.15 | 25.55 | 182.58 | 182.58 | 30.2 | 36.7% | 11,491.1 |
| | UC-06 | 2-hop FOAF | 53.59 | 25.47 | 573.96 | 573.96 | 18.7 | 40.9% | 11,547.6 |
| | UC-07 | Shortest Path | 182.26 | 97.46 | 689.55 | 689.55 | 5.5 | 83.8% | 11,653.2 |

---

## 4. Bảng So sánh Trực diện (Direct Comparison Matrix)

| Use Case | Latency TB: PG vs Mongo vs Neo4j (ms) | p99: PG vs Mongo vs Neo4j (ms) | QPS: PG vs Mongo vs Neo4j | CSDL Thắng thế |
| :--- | :---: | :---: | :---: | :---: |
| **UC-01 (Single Insert)** | 5.43 vs **5.22** vs 63.47 | 73.53 vs **40.66** vs 863.80 | 184.0 vs **191.7** vs 15.8 | **MongoDB** |
| **UC-02 (Point Read)** | **2.67** vs 2.90 vs 44.43 | 15.83 vs **8.82** vs 286.03 | **374.3** vs 345.3 vs 22.5 | **PostgreSQL** |
| **UC-03 (Join / Embedded Read)** | **3.28** vs 3.44 vs 66.18 | 23.94 vs **5.77** vs 433.19 | **304.7** vs 290.5 vs 15.1 | **PostgreSQL / MongoDB** |
| **UC-04 (Aggregation Group By)** | **55.01** vs 65.46 vs 128.00 | 200.51 vs **186.67** vs 579.54 | **18.2** vs 15.3 vs 7.8 | **PostgreSQL** |
| **UC-05 (1-hop Traversal)** | **2.17** vs 3.07 vs 33.15 | **6.29** vs 13.46 vs 182.58 | **459.9** vs 326.2 vs 30.2 | **PostgreSQL** |
| **UC-06 (2-hop FOAF)** | **6.30** vs 6.86 vs 53.59 | 28.96 vs **16.44** vs 573.96 | **158.6** vs 145.8 vs 18.7 | **PostgreSQL** |
| **UC-07 (Shortest Path)** | **7.07** vs 15.58 vs 182.26 | 33.46 vs **23.40** vs 689.55 | **141.5** vs 64.2 vs 5.5 | **PostgreSQL** |
