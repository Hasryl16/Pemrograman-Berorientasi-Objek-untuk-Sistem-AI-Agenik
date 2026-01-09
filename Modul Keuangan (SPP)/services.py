from datetime import datetime, timedelta
from models import db, Student, Billing, Payment
import hashlib
import hmac
import json
import os

# Billing amounts by program
BILLING_AMOUNTS = {
    'Teknik': 5000000,  # 5 million IDR
    'Ekonomi': 4000000  # 4 million IDR
}

def generate_billing(semester=None):
    """
    Generate billing for all active students at semester start
    """
    if not semester:
        # Auto-generate semester code (e.g., '2024-1' for Jan-Jun, '2024-2' for Jul-Dec)
        now = datetime.now()
        year = now.year
        semester_num = 1 if now.month <= 6 else 2
        semester = f"{year}-{semester_num}"

    # Get all active students
    active_students = Student.query.filter_by(status='active').all()

    billings_created = 0

    for student in active_students:
        # Check if billing already exists for this semester
        existing_billing = Billing.query.filter_by(
            student_id=student.id,
            semester=semester
        ).first()

        if existing_billing:
            continue  # Skip if billing already exists

        # Get billing amount based on program
        amount = BILLING_AMOUNTS.get(student.program_studi, 0)
        if amount == 0:
            continue  # Skip if program not recognized

        # Calculate due date (2 weeks after semester start)
        semester_start = datetime.now()
        due_date = semester_start + timedelta(weeks=2)

        # Create new billing
        new_billing = Billing(
            student_id=student.id,
            semester=semester,
            amount=amount,
            due_date=due_date,
            status='unpaid'
        )

        db.session.add(new_billing)
        billings_created += 1

    db.session.commit()
    return billings_created

def process_payment(billing_id, amount, method):
    """
    Process payment for a billing
    Returns payment result
    """
    try:
        # Get billing
        billing = Billing.query.get(billing_id)
        if not billing:
            return {"error": "Billing not found", "success": False}

        if billing.status == 'paid':
            return {"error": "Billing already paid", "success": False}

        # Calculate total paid so far
        total_paid = sum(payment.amount for payment in billing.payments)

        # Create new payment record
        new_payment = Payment(
            billing_id=billing_id,
            amount=amount,
            method=method,
            transaction_id=f"txn_{billing_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            status='completed'
        )

        # Update billing status
        new_total_paid = total_paid + amount

        if new_total_paid >= billing.amount:
            billing.status = 'paid'
        elif new_total_paid > 0:
            billing.status = 'partial'
        else:
            billing.status = 'unpaid'

        # Add payment and update billing
        db.session.add(new_payment)
        db.session.commit()

        return {
            "success": True,
            "billing_id": billing_id,
            "payment_id": new_payment.id,
            "transaction_id": new_payment.transaction_id,
            "amount_paid": amount,
            "total_paid": new_total_paid,
            "billing_status": billing.status,
            "remaining_amount": max(0, billing.amount - new_total_paid)
        }

    except Exception as e:
        db.session.rollback()
        return {"error": str(e), "success": False}

def verify_webhook_signature(payload, signature, secret):
    """
    Verify webhook signature for security
    """
    if not secret:
        return False

    # Create expected signature
    payload_str = json.dumps(payload, sort_keys=True)
    expected_signature = hmac.new(
        secret.encode(),
        payload_str.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected_signature)

def handle_webhook(payload):
    """
    Handle payment webhook notifications
    """
    try:
        # Extract data from payload
        transaction_id = payload.get('transaction_id')
        amount = payload.get('amount')
        status = payload.get('status')
        billing_id = payload.get('billing_id')
        method = payload.get('method', 'webhook')

        # Basic validation
        if not all([transaction_id, amount, status, billing_id]):
            return {"error": "Missing required fields in webhook payload", "success": False}

        if status != 'completed':
            return {"error": f"Payment status is {status}, not processing", "success": False}

        # Check if payment already exists
        existing_payment = Payment.query.filter_by(transaction_id=transaction_id).first()
        if existing_payment:
            return {"message": "Payment already processed", "success": True}

        # Process the payment
        result = process_payment(billing_id, amount, method)

        if result.get('success'):
            return {
                "success": True,
                "message": "Payment processed successfully",
                "transaction_id": transaction_id,
                "billing_status": result.get('billing_status')
            }
        else:
            return {"error": result.get('error'), "success": False}

    except Exception as e:
        return {"error": str(e), "success": False}
