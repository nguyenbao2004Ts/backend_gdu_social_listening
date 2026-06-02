from app.modules.users.repository import UserRepository


class AuthRepository:
    """Auth dùng chung bảng APP_USER — delegate sang UserRepository."""

    def __init__(self, user_repo: UserRepository) -> None:
        self._users = user_repo

    async def find_by_username(self, username: str):
        return await self._users.find_by_username(username)
