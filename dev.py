"""
Dev server — giống `nest start --watch` / `yarn start:dev`.
Chạy: yarn start:dev  |  python dev.py
Tắt:  Ctrl + C (cùng terminal)
"""

import os
from pathlib import Path

import uvicorn

ROOT = Path(__file__).resolve().parent
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8888"))
RELOAD = os.getenv("DEV_RELOAD", "1") == "1"


def main() -> None:
    print("GDU Social Listening API")
    print(f"  Local:   http://{HOST}:{PORT}")
    print(f"  Swagger: http://{HOST}:{PORT}/docs")
    print(f"  Reload:  {'on' if RELOAD else 'off'} (DEV_RELOAD=0 để tắt auto-reload, Ctrl+C sạch hơn trên Windows)")
    print("  Stop:    Ctrl + C\n")

    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=RELOAD,
        reload_dirs=[str(ROOT / "app")] if RELOAD else None,
    )


if __name__ == "__main__":
    main()
