from dataclasses import dataclass
from uuid import UUID

from app.common.settings import settings


@dataclass(eq=False)
class BaseException(Exception):
    @property
    def message(self):
        return 'An error ocured'


@dataclass(eq=False)
class ImageNotFoundException(BaseException):
    image_id: UUID

    @property
    def message(self):
        return f'Image was not found: {self.image_id}'


@dataclass(eq=False)
class UserIsNotOwnerException(BaseException):
    @property
    def message(self):
        return 'User is not an owner of image'


@dataclass(eq=False)
class ImageIsStillProcessingException(BaseException):
    @property
    def message(self):
        return 'Image is still processing'


@dataclass(eq=False)
class InvalidFileException(BaseException):
    @property
    def message(self):
        return 'File was not uploaded or file is not an image'


@dataclass(eq=False)
class ImageTooBigException(BaseException):
    @property
    def message(self):
        return f'Image can not be larger than {settings.MAX_FILE_SIZE_MB}MB'
