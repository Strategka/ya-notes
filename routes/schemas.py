from typing import Optional

from pydantic import BaseModel


class Base(BaseModel):
    class Config:
        orm_mode = True


class Note(Base):
    id: int
    title: Optional[str] = None
    content: str


class AddNote(Base):
    title: Optional[str] = None
    content: str

class EditNote(Base):
    title: Optional[str] = ''
    content: Optional[str] = ''
