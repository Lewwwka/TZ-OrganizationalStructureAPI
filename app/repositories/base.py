from typing import Generic, TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession

Model = TypeVar("Model")


class BaseRepository(Generic[Model]):
    def __init__(self, model: Type[Model], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id: int) -> Model | None:
        return await self.session.get(self.model, id)

    async def add(self, instance: Model) -> Model:
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def delete(self, instance: Model) -> None:
        await self.session.delete(instance)
        await self.session.flush()
