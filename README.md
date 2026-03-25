# 🚀 QDRANT VECTOR DATABASE - SEMINAR NHÓM 10
**Môn học:** Dữ liệu lớn (Big Data) | **Mã lớp:** IS405.Q23  
**Chủ đề:** Nghiên cứu và triển khai Qdrant trong hệ sinh thái Apache Spark.

---

## 📌 Mục lục
1. [Yêu cầu hệ thống](#1-yêu-cầu-hệ-thống)
2. [Hướng dẫn cài đặt (Docker)](#2-hướng-dẫn-cài-đặt-docker)
3. [Cấu hình Collection chuẩn](#3-cấu-hình-collection-chuẩn)
4. [Thông số kết nối cho Spark](#4-thông-số-kết-nối-cho-spark)
5. [Giải thích tham số kỹ thuật](#5-giải-thích-tham-số-kỹ-thuật)

---

## 1. Yêu cầu hệ thống
* Máy đã cài đặt [Docker Desktop](https://www.docker.com/products/docker-desktop/).
* Đảm bảo Docker đang ở trạng thái **Running** (biểu tượng con cá voi xanh dưới thanh Taskbar).

---

## 2. Hướng dẫn cài đặt (Docker)
Để đảm bảo dữ liệu không bị mất khi khởi động lại, mọi người thực hiện theo các bước sau:

**Bước 1:** Mở CMD hoặc PowerShell tại thư mục dự án và tạo thư mục lưu trữ dữ liệu:
```cmd
mkdir qdrant_storage
```

**Bước 2:** Chạy lệnh khởi tạo Container:
* Dành cho Windows CMD:
```cmd
docker run -d -p 6333:6333 -p 6334:6334 --name Qdrant -v "%cd%\qdrant_storage:/qdrant/storage:z" qdrant/qdrant
```

* Dành cho PowerShell:
```cmd
docker run -d -p 6333:6333 -p 6334:6334 --name Qdrant -v "${PWD}\qdrant_storage:/qdrant/storage:z" qdrant/qdrant
```

Kiểm tra: Sau khi chạy, truy cập Dashboard tại http://localhost:6333/dashboard để xác nhận Server đã hoạt động.

## 3. Cấu hình Collection chuẩn
Để đồng bộ với mã nguồn Spark của nhóm, mọi người tạo Collection thủ công trên Dashboard với các thông số sau:
```
Bước 1: Nhập Collection Name: Qdrant_Group10
Bước 2: Chọn Global search
Bước 3: Chọn Simple Single embedding
Bước 4: Dimensions (Size): 384
Bước 5: Distance Metric: Cosine
Bước 6: Nhấn Finish
```

## 4. Thông số kết nối cho Spark
Khi viết mã nguồn Spark ETL để đẩy dữ liệu, lưu ý cấu hình Endpoint như sau:
* **API URL:** http://localhost:6333
* **Embedding Model:** ```sentence-transformers/all-MiniLM-L6-v2```
* **Lưu ý:** Đảm bảo vector đầu ra có đúng ```384``` chiều trước khi upsert vào Qdrant.

## 5. Giải thích tham số kỹ thuật
* **Dimensions (384):** Số lượng chiều của không gian vector. Model MiniLM tạo ra 384 đặc trưng cho mỗi đối tượng, giúp cân bằng giữa hiệu năng và độ chính xác trên máy cá nhân.
* **Cosine Similarity:** Thuật toán tính toán độ tương đồng dựa trên góc giữa hai vector. Đây là metric tiêu chuẩn để tìm kiếm các văn bản có ý nghĩa gần giống nhau.
* **HNSW (Hierarchical Navigable Small World):** Thuật toán lập chỉ mục giúp tìm kiếm lân cận gần nhất với tốc độ cực nhanh trên tập dữ liệu lớn (>10.000 sản phẩm).
* **Volume Mapping (-v):** Ánh xạ dữ liệu từ Container vào thư mục máy thật (qdrant_storage), giúp dữ liệu bền vững ngay cả khi xóa/tạo lại Container.

© 2026 Nhóm 10 - Khoa Hệ thống Thông tin - UIT Người thực hiện: Nguyễn Văn Mạnh Huy (Leader)
