# Kiến trúc Backend (Module pattern)

## Luồng xử lý một request

```text
Client (Swagger / FE)
    → Controller   (HTTP: path, method, validate body)
    → Service      (nghiệp vụ, quy tắc, JWT, lỗi 404/401)
    → Repository   (Prisma: SELECT/INSERT/UPDATE/DELETE)
    → PostgreSQL
```

## Cấu trúc thư mục

```text
app/
├── main.py
├── core/                   # config, prisma, deps
├── schemas/                # Pydantic DTO (gom theo domain)
│   ├── auth.py
│   ├── users.py
│   └── keywords.py
├── api/v1/router.py        # Gộp route các module
└── modules/                # Mỗi folder = 1 chức năng
    ├── health/
    │   ├── controller.py
    │   ├── service.py
    │   └── repository.py
    ├── auth/
    ├── users/
    └── keywords/
```

## Vai trò từng file

| File | Vai trò | Ví dụ |
|------|---------|--------|
| **controller.py** | Route FastAPI, nhận `body`/`query`, gọi service | `@router.post("/login")` |
| **service.py** | Logic: login, hash password, map DTO | `AuthService.login()` |
| **repository.py** | Chỉ gọi Prisma, không if nghiệp vụ | `find_by_username()` |
| **app/schemas/*.py** | Pydantic: request/response JSON (tập trung, module import vào) | `LoginRequest`, `UserProfile` |

## Thêm module mới (vd: `dashboard`)

1. Tạo `app/modules/dashboard/` với `controller`, `service`, `repository`.
2. Thêm DTO trong `app/schemas/dashboard.py` (hoặc file tương ứng).
3. Trong `api/v1/router.py`: `include_router(dashboard_router, prefix="/dashboard")`.
4. Cập nhật `prisma/schema.prisma` → `prisma generate`.

## Module hiện có

| Module | Prefix API | Mô tả |
|--------|------------|--------|
| health | `/api/v1/health` | Kiểm tra API + DB |
| auth | `/api/v1/auth` | Login, profile |
| users | `/api/v1/users` | Danh sách user |
| keywords | `/api/v1/keywords` | CRUD từ khóa |
