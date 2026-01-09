from flask import Flask, request, jsonify
from flasgger import Swagger
from models import db
from services import process_payment, handle_webhook
from utils import analyze_payment_data
from scheduler import start_scheduler, stop_scheduler
from config import Config
import atexit

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app, config=swagger_config)

# Initialize database
db.init_app(app)

# Global scheduler variable
scheduler = None

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    ---
    tags:
      - Health
    responses:
      200:
        description: Service health status
        schema:
          type: object
          properties:
            status:
              type: string
              example: "healthy"
            service:
              type: string
              example: "billing-service"
    """
    return jsonify({"status": "healthy", "service": "billing-service"})

@app.route('/api/billing/generate', methods=['POST'])
def generate_billing_endpoint():
    """
    Generate billings for all active students
    ---
    tags:
      - Billing
    parameters:
      - name: body
        in: body
        required: false
        schema:
          type: object
          properties:
            semester:
              type: string
              description: Semester code (optional, auto-generated if not provided)
              example: "2024-1"
    responses:
      200:
        description: Billings generated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Successfully created 50 billings"
            billings_created:
              type: integer
              example: 50
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        from services import generate_billing
        semester = request.json.get('semester') if request.json else None
        billings_created = generate_billing(semester)
        return jsonify({
            "message": f"Successfully created {billings_created} billings",
            "billings_created": billings_created
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/payment/process', methods=['POST'])
def process_payment_endpoint():
    """
    Process payment for a billing
    ---
    tags:
      - Payment
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - billing_id
            - amount
            - method
          properties:
            billing_id:
              type: integer
              description: ID of the billing to pay
              example: 1
            amount:
              type: integer
              description: Payment amount in rupiah
              example: 4000000
            method:
              type: string
              description: Payment method
              example: "transfer"
    responses:
      200:
        description: Payment processed successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            billing_id:
              type: integer
              example: 1
            payment_id:
              type: integer
              example: 123
            transaction_id:
              type: string
              example: "txn_1_20240115120000"
            amount_paid:
              type: integer
              example: 4000000
            total_paid:
              type: integer
              example: 4000000
            billing_status:
              type: string
              example: "paid"
            remaining_amount:
              type: integer
              example: 0
      400:
        description: Bad request - missing or invalid data
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        billing_id = data.get('billing_id')
        amount = data.get('amount')
        method = data.get('method')

        if not all([billing_id, amount, method]):
            return jsonify({"error": "Missing required fields: billing_id, amount, method"}), 400

        result = process_payment(billing_id, amount, method)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/webhook/payment', methods=['POST'])
def webhook_payment():
    """Webhook endpoint for payment notifications"""
    try:
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "No payload provided"}), 400

        result = handle_webhook(payload)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analytics/payments', methods=['POST'])
def analyze_payments():
    """
    Analyze payment data from uploaded CSV file
    ---
    tags:
      - Analytics
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: CSV file with payment data (columns: nim, jumlah, tanggal, status)
    responses:
      200:
        description: Payment analysis completed successfully
        schema:
          type: object
          properties:
            total_revenue:
              type: string
              example: "Rp 250,000,000"
            collection_rate:
              type: string
              example: "85.5%"
            total_students:
              type: integer
              example: 100
            paid_students:
              type: integer
              example: 85
            top_debtors:
              type: array
              items:
                type: object
                properties:
                  nim:
                    type: string
                    example: "12345678"
                  nama:
                    type: string
                    example: "John Doe"
                  total_debt:
                    type: integer
                    example: 5000000
            recommendations:
              type: array
              items:
                type: string
                example: "Kirim reminder ke 15 mahasiswa dengan tunggakan >2 bulan"
      400:
        description: Bad request - invalid file or format
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        if not file.filename.endswith('.csv'):
            return jsonify({"error": "File must be CSV"}), 400

        # Save file temporarily
        import os
        temp_path = os.path.join('/tmp', 'payment_data.csv')
        file.save(temp_path)

        # Analyze data
        result = analyze_payment_data(temp_path)

        # Clean up
        os.remove(temp_path)

        return result, 200, {'Content-Type': 'application/json'}

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/students', methods=['GET'])
def get_students():
    """
    Get all students
    ---
    tags:
      - Students
    responses:
      200:
        description: List of all students
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nim:
                type: string
                example: "12345678"
              nama:
                type: string
                example: "John Doe"
              program_studi:
                type: string
                example: "Teknik"
              status:
                type: string
                example: "active"
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        from models import Student
        students = Student.query.all()
        result = [{
            "id": s.id,
            "nim": s.nim,
            "nama": s.nama,
            "program_studi": s.program_studi,
            "status": s.status
        } for s in students]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/billings', methods=['GET'])
def get_billings():
    """
    Get all billings
    ---
    tags:
      - Billings
    responses:
      200:
        description: List of all billings
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              student_nim:
                type: string
                example: "12345678"
              semester:
                type: string
                example: "2024-1"
              amount:
                type: integer
                example: 5000000
              due_date:
                type: string
                format: date-time
                example: "2024-02-15T00:00:00"
              status:
                type: string
                enum: [unpaid, partial, paid]
                example: "unpaid"
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        from models import Billing
        billings = Billing.query.all()
        result = [{
            "id": b.id,
            "student_nim": b.student.nim,
            "semester": b.semester,
            "amount": b.amount,
            "due_date": b.due_date.isoformat(),
            "status": b.status
        } for b in billings]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # Start scheduler
    scheduler = start_scheduler()

    # Register cleanup function
    atexit.register(lambda: stop_scheduler(scheduler))

    app.run(debug=True, host='0.0.0.0', port=5000)
