from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    program_studi = db.Column(db.String(50), nullable=False)  # Teknik or Ekonomi
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    billings = db.relationship('Billing', backref='student', lazy=True)

    def __repr__(self):
        return f'<Student {self.nim}: {self.nama}>'

class Billing(db.Model):
    __tablename__ = 'billings'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    semester = db.Column(db.String(20), nullable=False)  # e.g., '2024-1', '2024-2'
    amount = db.Column(db.Integer, nullable=False)  # in rupiah
    due_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='unpaid')  # unpaid, partial, paid
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    payments = db.relationship('Payment', backref='billing', lazy=True)

    def __repr__(self):
        return f'<Billing {self.id}: {self.student.nim} - {self.status}>'

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    billing_id = db.Column(db.Integer, db.ForeignKey('billings.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)  # payment amount
    method = db.Column(db.String(50), nullable=False)  # payment method
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(20), default='completed')  # completed, failed, pending
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Payment {self.transaction_id}: {self.amount}>'
