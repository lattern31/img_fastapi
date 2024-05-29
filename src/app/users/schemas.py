from typing import Optional
from uuid import UUID

from fastapi_users import schemas
from pydantic import EmailStr
from pydantic.json_schema import SkipJsonSchema


class UserRead(schemas.BaseUser[UUID]):
    id: UUID
    username: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    is_active: SkipJsonSchema[Optional[bool]] = True
    is_superuser: SkipJsonSchema[Optional[bool]] = False
    is_verified: SkipJsonSchema[Optional[bool]] = False


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str]
    is_active: SkipJsonSchema[Optional[bool]] = True
    is_superuser: SkipJsonSchema[Optional[bool]] = False
    is_verified: SkipJsonSchema[Optional[bool]] = False
