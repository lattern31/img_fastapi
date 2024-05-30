import io
import asyncio
from uuid import UUID

import PIL.Image
import PIL.ImageOps

from common.celery_worker import celery
from images.models import ImageEditActionEnum, ImageStatusEnum
from images.deps import get_image_repository
from common.database import scoped_session


@celery.task
def test_task(arg):
    print("in task", arg)


@celery.task
def edit_image_task(*args, **kwargs):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_edit_image(*args, **kwargs))


async def _edit_image(
    orig_id: UUID,
    new_id: UUID,
    action: ImageEditActionEnum,
):
    repository = await get_image_repository()
    async with scoped_session() as session:
        orig_image = await repository.get_meta(session, orig_id)
        new_image = await repository.get_meta(session, new_id)

    orig_image_bytes = await repository.file_repository.get(orig_image)
    pil_image = PIL.Image.open(io.BytesIO(orig_image_bytes))
    if action == ImageEditActionEnum.INVERT:
        edited_image = _invert_image(pil_image)
    else:
        edited_image = _rotate_image(pil_image, 90)
    imgByteArr = io.BytesIO()
    edited_image.save(imgByteArr, format="PNG")
    await repository.file_repository.save_bytes(
        new_image, imgByteArr.getvalue()
    )
    async with scoped_session() as session:
        await repository.update_status(
            session, id_=new_id, status=ImageStatusEnum.DONE
        )


def _rotate_image(image: PIL.Image.Image, angle: int) -> PIL.Image.Image:
    return image.transpose(method=PIL.Image.Transpose.ROTATE_90)


def _invert_image(image: PIL.Image.Image) -> PIL.Image.Image:
    if image.mode == "RGBA":
        r, g, b, a = image.split()
        rgb_image = PIL.Image.merge("RGB", (r, g, b))
        inverted_image = PIL.ImageOps.invert(rgb_image)
        r2, g2, b2 = inverted_image.split()
        final_transparent_image = PIL.Image.merge("RGBA", (r2, g2, b2, a))
        return final_transparent_image
    else:
        inverted_image = PIL.ImageOps.invert(image)
        return inverted_image
