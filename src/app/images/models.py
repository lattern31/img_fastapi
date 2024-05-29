from datetime import datetime, UTC
from dataclasses import dataclass, field
from enum import StrEnum, auto
from typing import Protocol
from uuid import UUID, uuid4


class ImageStatusEnum(StrEnum):
    PROCESSING = auto()
    DONE = auto()


class ImageEditActionEnum(StrEnum):
    INVERT = auto()
    ROTATE90 = auto()


class IImageFile(Protocol):
    content_type: str | None
    size: int | None

    async def read(self, size: int = -1) -> bytes: ...


@dataclass
class Image:
    owner_id: UUID
    title: str
    status: ImageStatusEnum = ImageStatusEnum.DONE
    id_: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    content_type: str = "image/png"
