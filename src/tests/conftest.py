from dataclasses import dataclass, field
from uuid import UUID

import pytest

from app.images.models import Image


@dataclass
class FakeImageFileRepository:
    _storage: dict[UUID, bytes] = field(default_factory=dict)

    async def save(self, image: Image, image_file):
        self._storage[image.id_] = image_file.read()

    async def save_bytes(self, image: Image, image_bytes: bytes):
        self._storage[image.id_] = image_bytes

    async def get(self, image: Image) -> bytes:
        return self._storage[image.id_]


@dataclass
class FakeImageRepository:
    _storage: dict[UUID, Image] = field(default_factory=dict)
    file_repository: FakeImageFileRepository = field(
        default_factory=FakeImageFileRepository
    )

    async def get_meta(self, session, id_):
        return self._storage.get(id_)

    async def create_meta(self, session, image):
        self._storage[image.id_] = image


@dataclass
class FakeImageFile:
    _bytes: bytes
    size: int
    content_type: str
    
    def read(self):
        return self._bytes


class FakeSession:
    pass


@pytest.fixture
def image_repository():
    return FakeImageRepository()
