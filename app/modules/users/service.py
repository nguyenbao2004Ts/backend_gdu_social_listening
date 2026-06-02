from typing import Any

from app.modules.users.repository import UserRepository
from app.schemas.users import UserProfile


def _to_profile(user: Any) -> UserProfile:
    return UserProfile(
        id=int(user.id),
        username=user.username,
        role=user.role,
        first_name=user.firstName,
        last_name=user.lastName,
        full_name=user.fullName,
        sdt=user.sdt,
        avatar_url=user.avatarUrl,
        sex=user.sex,
    )


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def list_users(self) -> list[UserProfile]:
        rows = await self._repo.find_all()
        return [_to_profile(u) for u in rows]

    async def get_by_username(self, username: str) -> UserProfile | None:
        user = await self._repo.find_by_username(username)
        if user is None:
            return None
        return _to_profile(user)

    async def create_user(
        self,
        *,
        username: str,
        password_hash: str,
        role: str,
        first_name: str | None = None,
        last_name: str | None = None,
        full_name: str | None = None,
        sdt: str | None = None,
        sex: str | None = None,
    ) -> UserProfile:
        row = await self._repo.create(
            {
                "username": username,
                "password": password_hash,
                "role": role,
                "firstName": first_name,
                "lastName": last_name,
                "fullName": full_name,
                "sdt": sdt,
                "sex": sex,
            },
        )
        return _to_profile(row)
