from flask import Flask, request, jsonify, send_file
from models import Session, Schedule, Student, Enrollment
from utils import generate_attendance_qr, validate_scan, generate_report, export_to_excel, ai_attendance_insights
from datetime import datetime

app = Flask(__name__)

@app.route('/attendance/qr/<int:schedule_id>', methods=['GET'])
def get_qr(schedule_id):
    img_buffer, token = generate_attendance_qr(schedule_id)
    return send_file(img_buffer, mimetype='image/png')

@app.route('/attendance/scan', methods=['POST'])
def scan_qr():
    data = request.get_json()
    token = data.get('token')
    nim = data.get('nim')

    if not token or not nim:
        return jsonify({'success': False, 'message': 'Missing token or nim'}), 400

    result = validate_scan(token, nim)
    return jsonify(result)

@app.route('/attendance/report/<course_id>', methods=['GET'])
def get_report(course_id):
    df = generate_report(course_id)
    return jsonify(df.to_dict(orient='index'))

@app.route('/attendance/export/<course_id>', methods=['GET'])
def export_report(course_id):
    data = export_to_excel(course_id)
    return jsonify(data)

@app.route('/attendance/insights/<course_id>', methods=['GET'])
def get_insights(course_id):
    insights = ai_attendance_insights(course_id)
    return jsonify(insights)

# Admin endpoints for setup (in production, add authentication)
@app.route('/admin/schedule', methods=['POST'])
def add_schedule():
    data = request.get_json()
    session = Session()
    schedule = Schedule(
        course_id=data['course_id'],
        date=data['date'],
        time=data['time'],
        location=data['location']
    )
    session.add(schedule)
    session.commit()
    schedule_id = schedule.id
    session.close()
    return jsonify({'id': schedule_id})

@app.route('/admin/student', methods=['POST'])
def add_student():
    data = request.get_json()
    session = Session()
    student = Student(nim=data['nim'], name=data['name'])
    session.add(student)
    session.commit()
    nim = student.nim
    session.close()
    return jsonify({'nim': nim})

@app.route('/admin/enrollment', methods=['POST'])
def add_enrollment():
    data = request.get_json()
    session = Session()
    enrollment = Enrollment(nim=data['nim'], course_id=data['course_id'])
    session.add(enrollment)
    session.commit()
    enrollment_id = enrollment.id
    session.close()
    return jsonify({'id': enrollment_id})

if __name__ == '__main__':
    app.run(debug=True)
