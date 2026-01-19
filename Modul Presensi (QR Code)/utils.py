import qrcode
import jwt
from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image
import os
from models import Session, Schedule, Student, Enrollment, Attendance

SECRET_KEY = 'your-secret-key-here'  # In production, use environment variable

def generate_attendance_qr(schedule_id, valid_minutes=15):
    payload = {
        'schedule_id': schedule_id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=valid_minutes)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    qr = qrcode.make(token)
    img_buffer = BytesIO()
    qr.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return img_buffer, token

def validate_scan(token, nim):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        schedule_id = payload['schedule_id']
        exp_time = datetime.fromtimestamp(payload['exp'])
    except jwt.ExpiredSignatureError:
        return {'success': False, 'message': 'QR code expired'}
    except jwt.InvalidTokenError:
        return {'success': False, 'message': 'Invalid QR code'}

    session = Session()
    schedule = session.query(Schedule).filter_by(id=schedule_id).first()
    if not schedule:
        session.close()
        return {'success': False, 'message': 'Schedule not found'}

    today = datetime.now().strftime('%Y-%m-%d')
    if schedule.date != today:
        session.close()
        return {'success': False, 'message': 'Schedule not for today'}

    enrollment = session.query(Enrollment).filter_by(nim=nim, course_id=schedule.course_id).first()
    if not enrollment:
        session.close()
        return {'success': False, 'message': 'Student not enrolled in this course'}

    existing_attendance = session.query(Attendance).filter_by(nim=nim, schedule_id=schedule_id).first()
    if existing_attendance:
        session.close()
        return {'success': False, 'message': 'Already scanned for this session'}

    now = datetime.utcnow()
    schedule_time = datetime.strptime(f"{schedule.date} {schedule.time}", "%Y-%m-%d %H:%M")
    time_diff = (now - schedule_time).total_seconds() / 60  # minutes

    if time_diff > 30:
        status = 'absent'
    elif time_diff > 15:
        status = 'terlambat'
    else:
        status = 'hadir'

    attendance = Attendance(nim=nim, schedule_id=schedule_id, status=status)
    session.add(attendance)
    session.commit()
    session.close()

    return {'success': True, 'status': status, 'message': f'Attendance recorded as {status}'}

def generate_report(course_id):
    session = Session()
    attendances = session.query(Attendance).join(Schedule).filter(Schedule.course_id == course_id).all()
    enrollments = session.query(Enrollment).filter_by(course_id=course_id).all()
    session.close()

    student_nims = [e.nim for e in enrollments]
    total_sessions = len(set(a.schedule_id for a in attendances))

    report_data = []
    for nim in student_nims:
        student_attendances = [a for a in attendances if a.nim == nim]
        hadir_count = sum(1 for a in student_attendances if a.status == 'hadir')
        terlambat_count = sum(1 for a in student_attendances if a.status == 'terlambat')
        percentage = (hadir_count + terlambat_count * 0.5) / total_sessions * 100 if total_sessions > 0 else 0
        warning = percentage < 75
        report_data.append({
            'NIM': nim,
            'Hadir': hadir_count,
            'Terlambat': terlambat_count,
            'Persentase': round(percentage, 2),
            'Warning': warning
        })

    return report_data

def export_to_excel(course_id):
    # Simplified: return data as JSON instead of Excel for now
    data = generate_report(course_id)
    return data  # In production, implement Excel export without pandas

def ai_attendance_insights(course_id):
    session = Session()
    attendances = session.query(Attendance).join(Schedule).filter(Schedule.course_id == course_id).all()
    session.close()

    insights = {
        'low_attendance_students': [],
        'patterns': [],
        'recommendations': []
    }

    # Analyze low attendance
    df = generate_report(course_id)
    low_attendance = df[df['Warning'] == True]
    insights['low_attendance_students'] = low_attendance['NIM'].tolist()

    # Simple pattern detection (can be enhanced with ML)
    day_patterns = {}
    for a in attendances:
        schedule = Session().query(Schedule).filter_by(id=a.schedule_id).first()
        Session().close()
        if schedule:
            day = datetime.strptime(schedule.date, '%Y-%m-%d').strftime('%A')
            if day not in day_patterns:
                day_patterns[day] = {'total': 0, 'absent': 0}
            day_patterns[day]['total'] += 1
            if a.status == 'absent':
                day_patterns[day]['absent'] += 1

    for day, data in day_patterns.items():
        absent_rate = data['absent'] / data['total'] * 100 if data['total'] > 0 else 0
        if absent_rate > 30:
            insights['patterns'].append(f"High absence rate on {day}: {absent_rate:.1f}%")
            insights['recommendations'].append(f"Consider rescheduling classes on {day}")

    # Generate recommendations
    if insights['low_attendance_students']:
        insights['recommendations'].append(f"Contact {len(insights['low_attendance_students'])} students for counseling")

    return insights
