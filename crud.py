from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

def get_calon_by_email(db: Session, email: str):
    return db.query(models.CalonMahasiswa).filter(models.CalonMahasiswa.email == email).first()

def create_calon(db: Session, calon_in: schemas.CalonCreate):
    if get_calon_by_email(db, calon_in.email):
        raise ValueError("Email already registered")
    calon = models.CalonMahasiswa(**calon_in.dict())
    db.add(calon)
    db.commit()
    db.refresh(calon)
    return calon

def get_calon(db: Session, id: int):
    return db.query(models.CalonMahasiswa).filter(models.CalonMahasiswa.id == id).first()

def approve_calon(db: Session, calon_id: int, nim_generator_callable):
    calon = get_calon(db, calon_id)
    if not calon:
        return None, "not_found"
    if calon.status == models.StatusEnum.approved:
        return calon, "already_approved"
    nim = nim_generator_callable(db, tahun=datetime.now().year, kode_prodi=calon.program_studi.kode)
    calon.nim = nim
    calon.status = models.StatusEnum.approved
    calon.approved_at = datetime.now()
    db.add(calon)
    db.commit()
    db.refresh(calon)
    return calon, "approved"
