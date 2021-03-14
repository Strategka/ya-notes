from typing import List, Optional

from fastapi import APIRouter, Response, status, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from . import schemas
from db.db import get_db
from db import models
from config.config import get_settings


router = APIRouter()
settings = get_settings()


def fill_notes(notes):
    for note in notes:
        if not note.title:
            setattr(note, 'title', note.content[:settings.show_n_chars])
    return notes


@router.post('/', 
             status_code=status.HTTP_201_CREATED, 
             response_model=schemas.Note,
             responses={
                 201: {'description': 'Note was successfully created'}
             }
)
def add_note(new_note: schemas.AddNote, db: Session = Depends(get_db)):
    note = models.Note(title = new_note.title, content = new_note.content)

    db.add(note)
    db.commit()
    
    return fill_notes([note])

@router.get('/', 
            response_model=List[schemas.Note],
            responses={
                200: {'description': 'Successfully return Notes'},
            }
)
def get_notes(query: Optional[str] = None, db: Session = Depends(get_db)):
    search_query = db.query(models.Note)
    if query:
        search_query = search_query.filter(or_(
            models.Note.title.like(f'%{query}%'), models.Note.content.like(f'%{query}%')
        ))
    notes = search_query.all()
    return fill_notes(notes)

@router.get('/{id}', 
            response_model=schemas.Note, 
            responses={
                200: {'description': 'Successfully return Note'},
                404: {'description': 'Note was not found'},
            }
)
def get_note(id: int, res: Response, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == id).first()
    if not note:
        res.status_code = status.HTTP_404_NOT_FOUND
        return
    setattr(note, 'title', note.content[:settings.show_n_chars])
    return note

@router.put('/{id}', 
            status_code = status.HTTP_202_ACCEPTED,
            responses={
                202: {'description': 'Note was successfully edited'},
                404: {'description': 'Note was not found'},
            }
)
def edit_note(id: int, edit_note: schemas.EditNote, res: Response, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == id).first()
    if not note:
        res.status_code = status.HTTP_404_NOT_FOUND
        return

    if 'title' in edit_note.dict():
        note.title = edit_note.title
    if 'content' in edit_note.dict():
        note.content = edit_note.content

    db.commit()


@router.delete('/{id}', 
               responses={
                   200: {'description': 'Note was successfully deleted'},
                   404: {'description': 'Note was not found'},
                }
)
def delete_note(id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == id).first()
    if not note:
        return
    
    db.delete(note)
    db.commit()
