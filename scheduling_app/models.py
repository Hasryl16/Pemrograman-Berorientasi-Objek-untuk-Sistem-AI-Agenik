from pydantic import BaseModel

class Schedule(BaseModel):
    id: int
    mata_kuliah: str
    hari: str
    jam_mulai: int
    jam_selesai: int
    ruangan: str
    kapasitas_ruangan: int
    dosen: str
    jumlah_mahasiswa: int