from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from common.settings import settings
from images.models import (
    ImageEditActionEnum,
    Image,
    ImageStatusEnum,
    IImageFile,
)
from images.repositories import IImageRepository, IImageFileRepository
from common.exceptions import (
    InvalidFileException,
    BadDataException,
    UserIsNotOwner,
    ImageIsStillProcessing,
)
from images.tasks import edit_image_task


async def get_image_meta(
    repository: IImageRepository,
    session: AsyncSession,
    image_id: UUID,
    owner_id: UUID,
) -> Image:
    image = await repository.get_meta(session=session, id_=image_id)
    if image is None:
        raise BadDataException(errors={"image_id": ["Image does not exist"]})
    if image.owner_id != owner_id:
        raise UserIsNotOwner(
            errors={"image_id": ["User is not an owner of image"]}
        )
    return image


async def get_image_file(
    repository: IImageFileRepository,
    image: Image,
) -> bytes:
    if image.status == ImageStatusEnum.PROCESSING:
        raise ImageIsStillProcessing(
            errors={"image_status": ["Image is still processing"]}
        )
    image_bytes = await repository.get(image)
    return image_bytes


async def create_image(
    repository: IImageRepository,
    session: AsyncSession,
    file: IImageFile,
    title: str,
    owner_id: UUID,
) -> UUID:
    if not file:
        raise InvalidFileException(errors={"file": ["File was not uploaded"]})
    if not file.content_type or file.content_type.partition("/")[0] != "image":
        raise InvalidFileException(errors={"file": ["File is not an image"]})
    if file.size is None:
        raise InvalidFileException(errors={"file": ["File has no size"]})
    if file.size / (1024 * 1024) > settings.MAX_FILE_SIZE_MB:
        raise InvalidFileException(
            errors={
                "file": [
                    f"File can't be more than {settings.MAX_FILE_SIZE_MB}MB"
                ]
            }
        )
    image = Image(title=title, owner_id=owner_id, status=ImageStatusEnum.DONE)
    await repository.create_meta(session, image)
    await repository.file_repository.save(image, file)
    return image.id_


async def edit_image(
    repository: IImageRepository,
    session: AsyncSession,
    id_: UUID,
    owner_id: UUID,
    new_title: str,
    action: ImageEditActionEnum,
) -> Image:
    new_image = Image(
        title=new_title, owner_id=owner_id, status=ImageStatusEnum.PROCESSING
    )
    await repository.create_meta(session, new_image)
    edit_image_task.delay(
        orig_id=id_,
        new_id=new_image.id_,
        action=action,
    )
    return new_image
