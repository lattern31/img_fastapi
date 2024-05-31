from uuid import uuid4
import pytest

from app.common.settings import settings
from app.images.services import (
    get_image_meta,
    get_image_file,
    create_image,
)
from app.images.models import Image, ImageStatusEnum
from app.images.exceptions import (
    ImageNotFoundException,
    UserIsNotOwnerException,
    ImageIsStillProcessingException,
    InvalidFileException,
    ImageTooBigException
)
from tests.conftest import FakeSession, FakeImageFile


@pytest.mark.asyncio
async def test_get_image_meta(image_repository):
    img = Image(title='', owner_id=uuid4())
    image_repository._storage[img.id_] = img
    img_new = await get_image_meta(
        image_repository,
        FakeSession(),
        image_id=img.id_,
        owner_id=img.owner_id
    )
    assert img == img_new

    fake_id = uuid4()
    with pytest.raises(ImageNotFoundException) as e:
        await get_image_meta(
            image_repository,
            FakeSession(),
            image_id=fake_id,
            owner_id=img.owner_id
        )
        assert e.message == ImageNotFoundException(fake_id).message

    fake_owner_id = uuid4()
    with pytest.raises(UserIsNotOwnerException):
        await get_image_meta(
            image_repository,
            FakeSession(),
            image_id=img.id_,
            owner_id=fake_owner_id
        )


@pytest.mark.asyncio
async def test_get_image_file(image_repository):
    img = Image(title='', owner_id=uuid4())
    image_repository._storage[img.id_] = img
    print(image_repository, image_repository.file_repository)
    image_repository.file_repository._storage[img.id_] = b'x10'
    img_bytes = await get_image_file(image_repository.file_repository, img)
    assert img_bytes == b'x10'
    img.status = ImageStatusEnum.PROCESSING
    with pytest.raises(ImageIsStillProcessingException):
        img_bytes = await get_image_file(image_repository.file_repository, img)


@pytest.mark.asyncio
async def test_create_image_file(image_repository):
    file = FakeImageFile(
        _bytes=b'x10', size=10, content_type='image/png'
    )
    owner_id = uuid4()
    img_id = await create_image(
        image_repository, FakeSession, file=file, title='', owner_id=owner_id
    )
    img = image_repository._storage[img_id]
    assert img.owner_id == owner_id
    assert img.title == ''
    assert file._bytes == image_repository.file_repository._storage[img_id]

    with pytest.raises(InvalidFileException):
        await create_image(
            image_repository,
            FakeSession,
            file=None,
            title='',
            owner_id=uuid4()
        )

    file = FakeImageFile(
        _bytes=b'x10', size=0, content_type='image/png'
    )
    with pytest.raises(InvalidFileException):
        await create_image(
            image_repository,
            FakeSession,
            file=file,
            title='',
            owner_id=uuid4()
        )

    file = FakeImageFile(
        _bytes=b'x10', size=10, content_type='video/mp4'
    )
    with pytest.raises(InvalidFileException):
        await create_image(
            image_repository,
            FakeSession,
            file=file,
            title='',
            owner_id=uuid4()
        )

    file = FakeImageFile(
        _bytes=b'x10',
        size=(settings.MAX_FILE_SIZE_MB * 1024 * 1024 + 1),
        content_type='image/png'
    )
    with pytest.raises(ImageTooBigException):
        img = await create_image(
            image_repository,
            FakeSession,
            file=file,
            title='',
            owner_id=uuid4()
        )
