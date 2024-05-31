import io
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.manager import current_active_verified_user
from app.db import get_async_session
from app.images.deps import get_image_repository
from app.images.services import (
    get_image_meta,
    get_image_file,
    create_image,
    edit_image,
)
from app.images.exceptions import (
    ImageNotFoundException,
    UserIsNotOwnerException,
    ImageIsStillProcessingException,
    InvalidFileException,
    ImageTooBigException
)
from app.images.models import Image
from app.images.schemas import ImageCreateSchema, ImageReadSchema, ImageEditSchema
from app.users.models import User


router = APIRouter()


async def valid_image_id(
    image_id: UUID,
    image_repository=Depends(get_image_repository),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_verified_user),
) -> Image:
    try:
        image = await get_image_meta(
            repository=image_repository,
            session=session,
            image_id=image_id,
            owner_id=user.id,
        )
    except ImageNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )
    except UserIsNotOwnerException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDEN, detail=e.message
        )
    return image


@router.post("/image")
async def create_image_handle(
    schema: ImageCreateSchema = Depends(),
    image_repository=Depends(get_image_repository),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_verified_user),
):
    try:
        image_id = await create_image(
            repository=image_repository,
            session=session,
            file=schema.file,
            title=schema.title,
            owner_id=user.id,
        )
    except (InvalidFileException, ImageTooBigException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        )
    return {"image_id": image_id}


@router.get("/image/{image_id}")
async def get_image_handler(
    image=Depends(valid_image_id),
    image_repository=Depends(get_image_repository),
) -> StreamingResponse:
    try:
        image_bytes = await get_image_file(
            image_repository.file_repository, image
        )
    except ImageIsStillProcessingException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        )
    return StreamingResponse(
        io.BytesIO(image_bytes), media_type=image.content_type
    )


@router.get("/images")
async def get_images_handler(
    image_repository=Depends(get_image_repository),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_verified_user),
) -> list[ImageReadSchema]:
    image_list = await image_repository.get_meta_list(
        session=session, owner_id=user.id
    )
    return image_list


@router.post("/image/{image_id}/edit")
async def edit_image_handler(
    schema: ImageEditSchema,
    image: Image = Depends(valid_image_id),
    image_repository=Depends(get_image_repository),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_verified_user),
) -> ImageReadSchema:
    new_image_meta = await edit_image(
        repository=image_repository,
        session=session,
        id_=image.id_,
        owner_id=user.id,
        new_title=schema.title,
        action=schema.action,
    )
    return new_image_meta


@router.get("/task-test")
async def test():
    from images.tasks import test_task

    test_task.delay(1)
    return 1
