from flask import Flask, request, jsonify
from models import Course, Student, KRS
from validators import SKSValidator, PrerequisiteValidator, ConflictValidator, DuplicateValidator
from state_machine import KRSStateMachine, KRSStatus

app = Flask(__name__)

# --- Simulasi data awal ---
student = Student(nim="12345", lulus=["Matematika Dasar"])
krs = KRS(student)
machine = KRSStateMachine()

# --- Chain of Responsibility setup ---
sks_validator = SKSValidator()
prereq_validator = sks_validator.set_next(PrerequisiteValidator())
conflict_validator = prereq_validator.set_next(ConflictValidator())
duplicate_validator = conflict_validator.set_next(DuplicateValidator())


# --- Helper: validasi sebelum simpan ---
def validate_krs():
    return sks_validator.handle(krs)


@app.route("/krs", methods=["GET"])
def get_krs():
    data = {
        "nim": krs.student.nim,
        "status": machine.state.name,
        "courses": [{"nama": c.nama, "sks": c.sks, "jadwal": c.jadwal, "prasyarat": c.prasyarat} for c in krs.courses],
        "total_sks": krs.total_sks()
    }
    return jsonify(data)


@app.route("/krs/add", methods=["POST"])
def add_course():
    data = request.get_json()
    nama = data.get("nama")
    sks = data.get("sks")
    jadwal = data.get("jadwal")
    prasyarat = data.get("prasyarat")

    course = Course(nama, sks, jadwal, prasyarat)
    krs.courses.append(course)

    validation = validate_krs()
    if not validation.success:
        krs.courses.pop()
        return jsonify({"success": False, "message": validation.message}), 400

    return jsonify({"success": True, "message": "Mata kuliah berhasil ditambahkan"})


@app.route("/krs/remove", methods=["DELETE"])
def remove_course():
    data = request.get_json()
    nama = data.get("nama")

    before = len(krs.courses)
    krs.courses = [c for c in krs.courses if c.nama != nama]
    after = len(krs.courses)

    if before == after:
        return jsonify({"success": False, "message": f"{nama} tidak ditemukan dalam KRS"}), 404
    return jsonify({"success": True, "message": f"{nama} berhasil dihapus dari KRS"})


@app.route("/krs/submit", methods=["POST"])
def submit_krs():
    validation = validate_krs()
    if not validation.success:
        return jsonify({"success": False, "message": validation.message}), 400
    try:
        machine.transition(KRSStatus.SUBMITTED)
        return jsonify({"success": True, "status": machine.state.name})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route("/krs/revision", methods=["POST"])
def revise_krs():
    try:
        machine.transition(KRSStatus.REVISION)
        return jsonify({"success": True, "status": machine.state.name})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route("/krs/approve", methods=["POST"])
def approve_krs():
    try:
        machine.transition(KRSStatus.APPROVED)
        return jsonify({"success": True, "status": machine.state.name})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
