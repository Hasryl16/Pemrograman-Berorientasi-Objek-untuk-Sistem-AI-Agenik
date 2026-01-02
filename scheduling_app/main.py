from fastapi import FastAPI, HTTPException
from models import Schedule
from services.scheduling import detect_schedule_conflict
from services.observer import (
    ScheduleSubject, StudentObserver,
    LecturerObserver, AdminObserver
)

app = FastAPI()

# =========================
# INIT GLOBAL STATE
# =========================
@app.on_event("startup")
def startup_event():
    app.state.schedules = []

# =========================
# OBSERVER SETUP
# =========================
subject = ScheduleSubject()
subject.attach(StudentObserver())
subject.attach(LecturerObserver())
subject.attach(AdminObserver())

# =========================
# POST SCHEDULE
# =========================
@app.post("/schedule")
def create_schedule(schedule: Schedule):
    schedules = app.state.schedules

    # 1️⃣ Cek kapasitas
    if schedule.jumlah_mahasiswa > schedule.kapasitas_ruangan:
        raise HTTPException(
            status_code=400,
            detail="Kapasitas ruangan tidak cukup"
        )

    # 2️⃣ Cek duplikasi
    for existing in schedules:
        if (
            existing.hari == schedule.hari and
            existing.jam_mulai == schedule.jam_mulai and
            existing.jam_selesai == schedule.jam_selesai and
            existing.ruangan == schedule.ruangan and
            existing.dosen == schedule.dosen
        ):
            raise HTTPException(
                status_code=409,
                detail="Jadwal sudah ada (duplicate schedule)"
            )

    # 3️⃣ CEK BENTROK (tanpa menyimpan)
    temp_schedules = schedules + [schedule]
    conflicts = detect_schedule_conflict(temp_schedules)

    if conflicts:
        raise HTTPException(
            status_code=409,
            detail={
                "message": "Jadwal bentrok, gagal ditambahkan",
                "conflicts": conflicts
            }
        )

    # 4️⃣ BARU SIMPAN JIKA AMAN
    schedules.append(schedule)

    subject.notify("SCHEDULE_CREATED", schedule.dict())

    return {
        "message": "Jadwal berhasil ditambahkan",
        "data": schedule
    }

# =========================
# GET ALL SCHEDULES
# =========================
@app.get("/schedule")
def get_all_schedules():
    return {
        "total": len(app.state.schedules),
        "data": app.state.schedules
    }
