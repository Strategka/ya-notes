from sqlalchemy.types import *
from sqlalchemy.schema import Column, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, Sequence('notes_id_seq'), primary_key=True)
    title = Column(String)
    content = Column(String, nullable=False)
