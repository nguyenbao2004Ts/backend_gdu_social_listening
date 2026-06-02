"""
Mỗi thư mục con = một chức năng (module) nghiệp vụ.

- controller.py  → HTTP routes (FastAPI)
- service.py     → Logic nghiệp vụ
- repository.py  → Truy vấn DB (Prisma)

DTO request/response: app/schemas/ (import vào controller/service).
"""
