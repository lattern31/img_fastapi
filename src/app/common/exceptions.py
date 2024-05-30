from dataclasses import dataclass


@dataclass(frozen=True)
class InvalidFileException(Exception):
    errors: dict[str, list[str]]


@dataclass(frozen=True)
class BadDataException(Exception):
    errors: dict[str, list[str]]


@dataclass(frozen=True)
class UserIsNotOwner(Exception):
    errors: dict[str, list[str]]


@dataclass(frozen=True)
class ImageIsStillProcessing(Exception):
    errors: dict[str, list[str]]
