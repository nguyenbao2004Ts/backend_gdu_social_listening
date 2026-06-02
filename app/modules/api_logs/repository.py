from prisma import Prisma


class ApiLogRepository:
    def __init__(self, db: Prisma) -> None:
        self._db = db

    async def create(
        self,
        *,
        name_log: str,
        request_method: str,
        request_url: str,
        input_data: str | None,
        output_data: str | None,
        user_create: int | None,
        status_code: int,
        execution_time: str,
    ) -> None:
        await self._db.apilog.create(
            data={
                "nameLog": name_log,
                "requestMethod": request_method,
                "requestUrl": request_url[:255],
                "input": input_data,
                "output": output_data,
                "userCreate": user_create,
                "statusCode": status_code,
                "executionTime": execution_time,
            },
        )
