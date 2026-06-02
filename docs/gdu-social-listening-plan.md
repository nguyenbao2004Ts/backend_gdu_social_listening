# GDU Social Listening - Technical Analysis & Development Plan

## 1. Tổng quan dự án

### Mục tiêu

Xây dựng hệ thống GDU Social Listening nhằm thu thập, lưu trữ, tìm kiếm và báo cáo các nội dung liên quan đến:

* GDU
* Đại học Gia Định
* Trường Đại học Gia Định
* Gia Định University
* Các từ khóa mở rộng khác

Phục vụ cho:

* Phòng Marketing
* Phòng Hành chính - Nhân sự
* Trung tâm Tuyển sinh
* Ban Giám hiệu

---

# 2. Phạm vi dữ liệu

## Google Reviews

Thu thập:

* Nội dung review
* Rating
* Người đánh giá
* Thời gian đánh giá
* Hình ảnh đính kèm (nếu có)

## Facebook Group

Ví dụ:

* GDU Confessions
* GDUers
* Cộng đồng Sinh viên Gia Định
* Tân sinh viên GDU

Thu thập:

* Bài viết
* Bình luận
* Số lượng tương tác
* Thời gian đăng
* Link nguồn

## Nguồn mở rộng

* Facebook Fanpage
* TikTok
* YouTube
* Website
* Diễn đàn
* Báo điện tử

---

# 3. Kiến trúc hệ thống đề xuất

## Kiến trúc tổng thể

Frontend (React)
↓
Backend API (FastAPI)
↓
PostgreSQL

Crawler Service (Python)
↓
Google Review
Facebook
YouTube
Website
TikTok

Scheduler (APScheduler/Cron)
↓
Crawl dữ liệu định kỳ

---

# 4. Công nghệ sử dụng

## Backend

* Python 3.12+
* FastAPI
* SQLAlchemy
* Pydantic
* JWT Authentication

## Database

* PostgreSQL bản 17.10.1
-> đã cài đặt thành công. Tạo database: gdu_social_listerning, schema: dev

## Frontend

* React
* Ant Design
* ECharts

## Crawler

* Requests
* BeautifulSoup
* Selenium
* Playwright

## Reporting

* Pandas
* OpenPyXL
* ReportLab

## Deployment

* Docker
* Docker Compose
* Ubuntu Server

---

# 5. Module chức năng

## Module 1 - Authentication

### Chức năng

* Đăng nhập
* Đăng xuất
* JWT Authentication
* Quản lý người dùng

### Vai trò

#### Root Admin

* Toàn quyền hệ thống

#### Marketing

* Xem Dashboard
* Tìm kiếm dữ liệu
* Xuất báo cáo

#### Nhân sự

* Xem Dashboard
* Xem dữ liệu

#### Tuyển sinh

* Xem Dashboard
* Xem dữ liệu tuyển sinh

---

## Module 2 - Quản lý từ khóa

### Chức năng

* Thêm từ khóa
* Cập nhật từ khóa
* Xóa từ khóa
* Bật/Tắt theo dõi

### Ví dụ

* GDU
* Đại học Gia Định
* Gia Định University

---

## Module 3 - Thu thập dữ liệu

### Chức năng

* Crawl thủ công
* Crawl tự động
* Lưu lịch sử crawl
* Theo dõi trạng thái crawler

### Scheduler

* Chạy mỗi ngày
* Chạy theo giờ
* Chạy theo cấu hình

---

## Module 4 - Tìm kiếm dữ liệu

### Tìm theo

* Keyword
* Thời gian
* Nguồn dữ liệu
* Loại dữ liệu

### Kết quả

Hiển thị:

* Tiêu đề
* Nội dung
* Người đăng
* Link nguồn
* Thời gian

---

## Module 5 - Dashboard

### KPI

* Tổng số đề cập
* Tổng số bài viết
* Tổng số bình luận
* Tổng số nguồn dữ liệu

### Biểu đồ

#### Theo thời gian

* Ngày
* Tuần
* Tháng

#### Theo nguồn

* Google Reviews
* Facebook
* YouTube
* TikTok
* Website

### Top dữ liệu

* Top từ khóa
* Top bài viết tương tác cao
* Top chủ đề nổi bật

---

## Module 6 - Báo cáo

### Xuất dữ liệu

* Excel
* CSV
* PDF

### Nội dung

* Dashboard
* Bảng thống kê
* Danh sách bài viết
* Danh sách review

---

# 6. Thiết kế Database

## users

| Column     | Type      |
| ---------- | --------- |
| id         | bigint    |
| username   | varchar   |
| password   | varchar   |
| role       | varchar   | -> admin/ marketing - hr - admissions
| created_at | timestamp |
| updated_at | timestamp |


---

## keywords

| Column     | Type      |
| ---------- | --------- |
| id         | bigint    |
| keyword    | varchar   |
| status     | boolean   |
| created_at | timestamp |

---

## sources

| Column | Type    |
| ------ | ------- |
| id     | bigint  |
| name   | varchar |
| type   | varchar |

---

## social_posts

| Column            | Type      |
| ----------------- | --------- |
| id                | bigint    |
| source_id         | bigint    |
| keyword           | varchar   |
| title             | text      |
| content           | longtext  |
| author            | varchar   |
| url               | text      |
| interaction_count | integer   |
| post_time         | timestamp |
| crawl_time        | timestamp |

---

## comments

| Column       | Type      |
| ------------ | --------- |
| id           | bigint    |
| post_id      | bigint    |
| author       | varchar   |
| content      | text      |
| created_time | timestamp |

---

## google_reviews

| Column         | Type      |
| -------------- | --------- |
| id             | bigint    |
| reviewer       | varchar   |
| rating         | integer   |
| review_content | text      |
| review_time    | timestamp |
| image_url      | text      |

---

## crawl_logs

| Column        | Type      |
| ------------- | --------- |
| id            | bigint    |
| source_name   | varchar   |
| status        | varchar   |
| total_records | integer   |
| started_at    | timestamp |
| finished_at   | timestamp |

## api_logs
| id | bigint |
| name_log | varchar(255) |
| request_method | varchar(10) |
| request_url | varchar(255) |
| input | longtext |
| output | longtext |
| user_create | bigint |
| created_at | timestamp |
| status_code | int |
| execution_time | varchar(50) |

---

# 7. API dự kiến

## Authentication

POST /api/auth/login

POST /api/auth/logout

GET /api/auth/profile

---

## User

GET /api/users

POST /api/users

PUT /api/users/{id}

DELETE /api/users/{id}

---

## Keyword

GET /api/keywords

POST /api/keywords

PUT /api/keywords/{id}

DELETE /api/keywords/{id}

---

## Search

GET /api/search

---

## Dashboard

GET /api/dashboard/summary

GET /api/dashboard/chart

GET /api/dashboard/top-posts

GET /api/dashboard/top-keywords

---

## Reports

GET /api/reports/excel

GET /api/reports/csv

GET /api/reports/pdf

---

# 8. Kế hoạch thực hiện 01 tháng

## Tuần 1

* Phân tích yêu cầu
* Thiết kế database
* Xây dựng Authentication
* Quản lý User
* Quản lý Keyword

## Tuần 2

* Xây dựng Google Review Crawler
* Xây dựng Website Crawler
* Lưu dữ liệu vào Database

## Tuần 3

* Dashboard
* Search
* API thống kê

## Tuần 4

* Export Excel
* Export CSV
* Export PDF
* Docker Deploy
* Tài liệu hướng dẫn
* Demo hệ thống

---

# 9. Rủi ro cần làm rõ

## Facebook Group

* Public hay Private?
* Có quyền quản trị nhóm không?

## Google Review

* Chỉ theo dõi review của GDU?
* Hay nhiều địa điểm khác?

## Dashboard

* Realtime hay cập nhật theo lịch?

## Keyword

* Người dùng có được tự tạo keyword không?

## Phân quyền

* Marketing có được export dữ liệu không?
* Nhân sự được xem những nguồn nào?

---

# 10. Kết quả bàn giao

* Source Code
* Database
* Dashboard
* Tài liệu hướng dẫn sử dụng
* Tài liệu kiến trúc hệ thống
* Docker Deployment
* Demo trên IP nội bộ
