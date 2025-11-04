from sqlalchemy.orm import Session
from . import models
from sqlalchemy.exc import IntegrityError

def generate_nim(db: Session, tahun: int, kode_prodi: str) -> str:
    kode = kode_prodi.zfill(3)[:3]
    while True:
        seq_row = db.query(models.NIMSequence).filter(models.NIMSequence.tahun == tahun, models.NIMSequence.kode_prodi == kode).first()
        if seq_row:
            seq_row.seq += 1
            db.add(seq_row)
            try:
                db.commit()
                break
            except IntegrityError:
                db.rollback()
                continue
        else:
            seq_row = models.NIMSequence(tahun=tahun, kode_prodi=kode, seq=1)
            db.add(seq_row)
            try:
                db.commit()
                db.refresh(seq_row)
                break
            except IntegrityError:
                db.rollback()
                continue
    nim = f"{tahun}{kode}-{seq_row.seq:04d}"
    return nim
