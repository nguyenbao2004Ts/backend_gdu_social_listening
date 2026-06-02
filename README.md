# GDU Social Listening (Backend)

Thư mục **`gdu_social_listerning`** là project backend: FastAPI + Prisma + PostgreSQL.  
Tài liệu nghiệp vụ: [docs/gdu-social-listening-plan.md](docs/gdu-social-listening-plan.md).

---

## Cấu trúc

```text
gdu_social_listerning/
├── app/
│   ├── main.py
│   ├── core/                 # config, prisma, deps
│   ├── schemas/              # Pydantic DTO
│   ├── api/v1/router.py
│   └── modules/              # auth, users, keywords, health
├── prisma/schema.prisma
├── dev.py                    # yarn start:dev → entry dev server
├── package.json              # scripts: start:dev, stop:dev
├── scripts/run-dev.ps1
├── .env                      # không commit
└── docs/ARCHITECTURE.md
```

---

## Yêu cầu (cài 1 lần trên máy)

| # | Công cụ | Ghi chú |
|---|---------|---------|
| 1 | **Python 3.12.x** | Tick **Add python.exe to PATH** khi cài |
| 2 | **PostgreSQL 17** | DB `gdu_social_listening`, schema `dev` |
| 3 | **Node.js 20+** | `yarn start:dev` hoặc `npm run start:dev` — hoặc chỉ `python dev.py` |

### Python — nếu terminal báo "Python was not found"

1. **Settings → App execution aliases** → tắt `python.exe` và `python3.exe` (Microsoft Store).
2. **Tắt hết Cursor** → mở lại → terminal mới.
3. Kiểm tra: `python --version` → `Python 3.12.x`.

Hoặc dùng đường dẫn đầy đủ:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" --version
```

---

## Thứ tự cài đặt & chạy (PowerShell)

Mở terminal tại thư mục project. Chạy **lần lượt từ Bước 1 → 8**.

### Bước 1 — Vào thư mục project

```powershell
cd c:\Users\baong\gdu_work\thucviec_gdu\gdu_social_listerning
```

### Bước 2 — Kiểm tra Python

```powershell
python --version
```

Kỳ vọng: `Python 3.12.x`

### Bước 3 — Tạo virtual environment

```powershell
python -m venv .venv
```

### Bước 4 — Bật venv

```powershell
.\.venv\Scripts\Activate.ps1
```

Nếu lỗi execution policy:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

Prompt có `(.venv)` ở đầu dòng là đúng.

### Bước 5 — Cài thư viện Python

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> Phải xong bước này **trước** khi chạy `prisma generate` (nếu không sẽ lỗi `No module named prisma.__main__`).

### Bước 6 — Cấu hình `.env`

Copy **toàn bộ** từ `.env.example` sang `.env` (app **bắt buộc** có file `.env`, không dùng default trong code). Sửa ít nhất `DATABASE_URL` và `JWT_SECRET`:

```powershell
Copy-Item .env.example .env
```

### Bước 7 — Generate Prisma Client

```powershell
python -m prisma generate
```

Kiểm tra thêm (tùy chọn):

```powershell
python -m prisma validate
```

### Bước 8 — Chạy API (giống NestJS: `yarn start:dev`)

**Cách khuyên dùng** — một lệnh, tắt bằng **Ctrl + C** (cùng terminal):

```powershell
yarn start:dev
```

Không có Yarn → dùng npm:

```powershell
npm run start:dev
```

Hoặc không cần Node:

```powershell
python dev.py
```

Hoặc:

```powershell
.\scripts\run-dev.ps1
```

> FastAPI vẫn cần ASGI server bên trong (uvicorn) — giống NestJS vẫn chạy trên Node. Bạn **không gõ uvicorn trực tiếp** nữa; mọi thứ qua `dev.py` / `yarn start:dev`.

**Tắt server:** `Ctrl + C` trong terminal đang chạy (đủ trong hầu hết trường hợp).

Nếu port vẫn bị kẹt (Windows + `--reload` đôi khi sót process):

```powershell
yarn stop:dev
```

Trên Windows nếu Ctrl+C vẫn hay sót process, tắt auto-reload (1 process, dễ kill hơn):

```powershell
$env:DEV_RELOAD="0"; yarn start:dev
```

| Kiểm tra | URL |
|----------|-----|
| Swagger (test API) | http://127.0.0.1:8888/docs |
| Health (API + DB) | http://127.0.0.1:8888/api/v1/health |
| ReDoc | http://127.0.0.1:8888/redoc |

### Swagger — đăng nhập (ổ khóa)

1. `POST /api/v1/auth/login` → copy `access_token` (gọi API) và `refresh_token` (đổi token, hạn 24h)
2. Bấm **Authorize** (góc phải) → dán: `Bearer <access_token>` hoặc chỉ token (tùy UI)
3. Gọi API có **ổ khóa** (`/users`, `/keywords`, `/auth/profile`)
4. Khi `access_token` hết hạn: `POST /api/v1/auth/refresh` body `{ "refresh_token": "..." }` → cặp token mới

API public (không khóa): `/health`, `/auth/login`, `/auth/register`, `/auth/refresh`. Mọi request (trừ `/docs`) được ghi vào bảng `API_LOGS`.

---

## Lần sau mở máy (giống Nest)

```powershell
cd c:\Users\baong\gdu_work\thucviec_gdu\gdu_social_listerning
yarn start:dev
```

Tắt: **Ctrl + C**

---

## Copy-paste nhanh (lần đầu, đã cài Python + PostgreSQL)

```powershell
cd c:\Users\baong\gdu_work\thucviec_gdu\gdu_social_listerning
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m prisma generate
yarn start:dev
```

---

## Tạo user admin (đăng nhập Swagger)

Password trong DB phải là **bcrypt hash** (venv đã bật):

```powershell
python -c "from passlib.context import CryptContext; print(CryptContext(schemes=['bcrypt']).hash('admin123'))"
```

Navicat → `dev."APP_USER"` → INSERT user với `password` = chuỗi hash vừa in.

---

## API (v1)

| Method | Path |
|--------|------|
| GET | `/api/v1/health` |
| POST | `/api/v1/auth/login` | Trả `access_token` + `refresh_token` (24h) |
| POST | `/api/v1/auth/refresh` | Đổi refresh → token mới (public) |
| POST | `/api/v1/auth/register` | Tạo tài khoản (public) |
| GET | `/api/v1/auth/profile` | Cần JWT |
| CRUD | `/api/v1/keywords` |
| GET | `/api/v1/users` |

---

---

## Module sắp tới

`app/modules/dashboard/` + `app/schemas/dashboard.py` → đăng ký trong `app/api/v1/router.py`.

Chi tiết kiến trúc: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).
