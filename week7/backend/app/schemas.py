from datetime import datetime

from pydantic import BaseModel, ConfigDict, constr

NonEmptyShortText = constr(strip_whitespace=True, min_length=1, max_length=200)
NonEmptyLongText = constr(strip_whitespace=True, min_length=1, max_length=2000)
SearchText = constr(strip_whitespace=True, min_length=1, max_length=200)


class NoteCreate(BaseModel):
    title: NonEmptyShortText
    content: NonEmptyLongText
    project_id: int | None = None


class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    project_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NotePatch(BaseModel):
    title: NonEmptyShortText | None = None
    content: NonEmptyLongText | None = None
    project_id: int | None = None


class ActionItemCreate(BaseModel):
    description: NonEmptyLongText
    project_id: int | None = None


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool
    project_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ActionItemPatch(BaseModel):
    description: NonEmptyLongText | None = None
    completed: bool | None = None
    project_id: int | None = None


class ProjectCreate(BaseModel):
    name: NonEmptyShortText
    description: NonEmptyLongText


class ProjectRead(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectPatch(BaseModel):
    name: NonEmptyShortText | None = None
    description: NonEmptyLongText | None = None
