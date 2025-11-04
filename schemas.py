from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import date, datetime
import re

PHONE_REGEX = re.compile(r'^(?:\+62|62|0)\d{8,13}$')

class CalonCreate(BaseModel):
    nama_lengkap: str
    email: EmailStr
    phone: str
    tanggal_lahir: Optional[date]
    alamat: Optional[str] = None
    program_studi_id: int
    jalur_masuk_id: int

    @validator("phone")
    def validate_phone(cls, v: str):
        v = v.strip()
        if not PHONE_REGEX.match(v):
            raise ValueError("Format phone invalid. Contoh: 081234567890 atau +6281234567890")
        if v.startswith("0"):
            v = "62" + v[1:]
        elif v.startswith("+"):
            v = v[1:]
        return v

class CalonOut(BaseModel):
    id: int
    nama_lengkap: str
    email: EmailStr
    phone: str
    tanggal_lahir: Optional[date]
    alamat: Optional[str]
    program_studi_id: int
    jalur_masuk_id: int
    status: str
    nim: Optional[str]
    created_at: Optional[datetime]
    approved_at: Optional[datetime]

    class Config:
        orm_mode = True
