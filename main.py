from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, crud, utils
from .database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PMB API", version="1.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/pmb/register", response_model=schemas.CalonOut, status_code=status.HTTP_201_CREATED)
def register(calon_in: schemas.CalonCreate, db: Session = Depends(get_db)):
    try:
        calon = crud.create_calon(db, calon_in)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return calon

@app.get("/api/pmb/status/{id}", response_model=schemas.CalonOut)
def status(id: int, db: Session = Depends(get_db)):
    calon = crud.get_calon(db, id)
    if not calon:
        raise HTTPException(status_code=404, detail="Calon tidak ditemukan")
    return calon

@app.put("/api/pmb/approve/{id}", response_model=schemas.CalonOut)
def approve(id: int, db: Session = Depends(get_db)):
    def nim_callable(session_db, tahun, kode_prodi):
        return utils.generate_nim(session_db, tahun, kode_prodi)
    calon, reason = crud.approve_calon(db, id, nim_callable)
    if reason == "not_found":
        raise HTTPException(status_code=404, detail="Calon tidak ditemukan")
    elif reason == "already_approved":
        raise HTTPException(status_code=400, detail="Calon sudah disetujui")
    return calon
