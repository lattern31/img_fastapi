from app.images.repositories import (
    IImageRepository,
    ImageRepository,
    ImageFileRepository,
)


async def get_image_repository() -> IImageRepository:
    file_repository = ImageFileRepository()
    return ImageRepository(file_repository)
