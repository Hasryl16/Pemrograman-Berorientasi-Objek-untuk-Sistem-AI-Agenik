from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from .database import Base

class StatusEnum(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class JalurMasuk(Base):
    __tablename__ = "jalur_masuk"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(50), unique=True, nullable=False)

class ProgramStudi(Base):
    __tablename__ = "program_studi"
    id = Column(Integer, primary_key=True, index=True)
    kode = Column(String(10), unique=True, nullable=False)
    nama = Column(String(100), nullable=False)
    fakultas = Column(String(100), nullable=True)

class CalonMahasiswa(Base):
    __tablename__ = "calon_mahasiswa"
    id = Column(Integer, primary_key=True, index=True)
    nama_lengkap = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, unique=True, index=True)
    phone = Column(String(50), nullable=False)
    tanggal_lahir = Column(Date, nullable=True)
    alamat = Column(String(500), nullable=True)
    program_studi_id = Column(Integer, ForeignKey("program_studi.id"), nullable=False)
    jalur_masuk_id = Column(Integer, ForeignKey("jalur_masuk.id"), nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending, nullable=False)
    nim = Column(String(50), nullable=True, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    approved_at = Column(DateTime(timezone=True), nullable=True)

    program_studi = relationship("ProgramStudi")
    jalur_masuk = relationship("JalurMasuk")

class NIMSequence(Base):
    __tablename__ = "nim_sequence"
    id = Column(Integer, primary_key=True, index=True)
    tahun = Column(Integer, nullable=False)
    kode_prodi = Column(String(10), nullable=False)
    seq = Column(Integer, default=0, nullable=False)
    __table_args__ = (UniqueConstraint("tahun", "kode_prodi", name="uq_tahun_kode"),)
