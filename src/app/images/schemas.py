from datetime import datetime
from uuid import UUID

from fastapi import File, UploadFile
from pydantic import BaseModel, Field

from images.models import ImageStatusEnum, ImageEditActionEnum


class BaseImage(BaseModel):
    title: str


class ImageCreateSchema(BaseImage):
    file: UploadFile = File(...)


class ImageReadSchema(BaseImage):
    id: UUID = Field(validation_alias="id_")
    status: ImageStatusEnum
    created_at: datetime


class ImageEditSchema(BaseImage):
    action: ImageEditActionEnum
