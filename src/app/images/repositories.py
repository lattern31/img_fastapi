from typing import Protocol
from pathlib import Path
from dataclasses import dataclass, asdict
import datetime
from uuid import UUID

import aiofiles
from sqlalchemy import ForeignKey, select, update, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

from images.models import Image, ImageStatusEnum, IImageFile
from common.settings import settings
from common.database import Base


class IImageFileRepository(Protocol):
    async def save(self, image: Image, image_file: IImageFile) -> None: ...

    async def save_bytes(self, image: Image, image_bytes: bytes) -> None: ...

    async def get(self, image: Image) -> bytes: ...


class IImageRepository(Protocol):
    file_repository: IImageFileRepository

    async def create_meta(
        self, session: AsyncSession, image: Image
    ) -> None: ...

    async def get_meta_list(
        self, session: AsyncSession, owner_id: UUID
    ) -> list[Image]: ...

    async def get_meta(
        self, session: AsyncSession, id_: UUID
    ) -> Image | None: ...

    async def update_status(
        self, session: AsyncSession, id_: UUID, status: ImageStatusEnum
    ) -> None: ...


class ImageTable(Base):
    __tablename__ = "image"

    id_: Mapped[UUID] = mapped_column(primary_key=True)
    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_.id", ondelete="CASCADE"),
    )
    title: Mapped[str]
    status: Mapped[ImageStatusEnum]
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True)
    )


class ImageFileRepository:
    def _get_path(self, image: Image) -> Path:
        return settings.IMAGE_DIR_PATH / str(image.id_)

    async def save(self, image: Image, image_file: IImageFile) -> None:
        path = self._get_path(image)
        async with aiofiles.open(path, "wb") as f:
            while chunk := await image_file.read(settings.FILE_CHUNK_SIZE):
                await f.write(chunk)

    async def save_bytes(self, image: Image, image_bytes: bytes) -> None:
        path = self._get_path(image)
        async with aiofiles.open(path, "wb") as f:
            await f.write(image_bytes)

    async def get(self, image: Image) -> bytes:
        path = self._get_path(image)
        async with aiofiles.open(path, "rb") as f:
            return await f.read()


@dataclass
class ImageRepository:
    file_repository: IImageFileRepository

    def _table_to_model(self, image_rep: ImageTable) -> Image:
        return Image(
            id_=image_rep.id_,
            title=image_rep.title,
            owner_id=image_rep.owner_id,
            status=image_rep.status,
            created_at=image_rep.created_at,
        )

    async def create_meta(self, session: AsyncSession, image: Image) -> None:
        image_rep = ImageTable(**asdict(image))
        session.add(image_rep)
        await session.commit()

    async def get_meta_list(
        self, session: AsyncSession, owner_id: UUID
    ) -> list[Image]:
        statement = select(ImageTable).where(ImageTable.owner_id == owner_id)
        images_rep = (await session.execute(statement)).scalars()
        return [self._table_to_model(i) for i in images_rep]

    async def get_meta(self, session: AsyncSession, id_: UUID) -> Image | None:
        image_rep = await session.get(ImageTable, id_)
        if image_rep is None:
            return None
        image = self._table_to_model(image_rep)
        return image

    async def update_status(
        self, session: AsyncSession, id_: UUID, status: ImageStatusEnum
    ) -> None:
        statement = (
            update(ImageTable)
            .where(ImageTable.id_ == id_)
            .values(status=status)
        )
        await session.execute(statement)
        await session.commit()
