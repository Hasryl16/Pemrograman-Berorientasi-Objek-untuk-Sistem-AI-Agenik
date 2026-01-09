# Student Billing System (SPP)

A comprehensive billing and payment management system for educational institutions, built with Flask and SQLAlchemy.

## Features

- **Automatic Billing Generation**: Creates bills for all active students at semester start
- **Program-Specific Pricing**: Teknik (5 million IDR), Ekonomi (4 million IDR)
- **Payment Processing**: Handles partial and full payments with status tracking
- **Webhook Integration**: Secure payment notifications with signature verification
- **Data Analytics**: CSV-based payment analysis with insights and recommendations
- **Scheduled Tasks**: APScheduler for automated semester billing

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` file with your configuration:
   ```env
   SECRET_KEY=your-secret-key-here
   FLASK_ENV=development
   DATABASE_URL=sqlite:///billing.db
   WEBHOOK_SECRET=your-webhook-secret-here
   SCHEDULER_TIMEZONE=Asia/Jakarta
   ```

## Running the Application

### Option 1: Using the main app.py (Recommended for development)

```bash
python app.py
```

### Option 2: Using run.py

```bash
python run.py
```

The application will start on `http://localhost:5000` (or `http://0.0.0.0:5000`)

## API Endpoints

### Health Check
- `GET /health` - Check service status

### Billing Management
- `POST /api/billing/generate` - Manually generate billings
- `GET /api/billings` - Get all billings

### Payment Processing
- `POST /api/payment/process` - Process payments
- `POST /api/webhook/payment` - Handle payment webhooks

### Data Analytics
- `POST /api/analytics/payments` - Upload CSV for analysis

### Student Management
- `GET /api/students` - Get all students

## Testing the Application

### 1. Health Check
```bash
curl http://localhost:5000/health
```

### 2. Generate Sample Billings
```bash
curl -X POST http://localhost:5000/api/billing/generate \
  -H "Content-Type: application/json" \
  -d '{"semester": "2024-1"}'
```

### 3. Process a Payment
```bash
curl -X POST http://localhost:5000/api/payment/process \
  -H "Content-Type: application/json" \
  -d '{
    "billing_id": 1,
    "amount": 4000000,
    "method": "transfer"
  }'
```

### 4. Upload Payment Data for Analysis
```bash
curl -X POST http://localhost:5000/api/analytics/payments \
  -F "file=@sample_payment_data.csv"
```

## Database

The application uses SQLite by default (`billing.db`). To use a different database, update the `DATABASE_URL` in your `.env` file.

Tables created automatically:
- `students` - Student information
- `billings` - Billing records
- `payments` - Payment transactions

## Scheduler

The APScheduler runs automatically and generates billings at:
- January 1st (Semester 1 start)
- July 1st (Semester 2 start)

## Sample Data

Use `sample_payment_data.csv` to test the analytics endpoint. The CSV should contain columns:
- `nim`: Student ID
- `jumlah`: Payment amount
- `tanggal`: Payment date
- `status`: Payment status

## Development

### Adding Sample Students

You can add students programmatically or through database queries. Example:

```python
from app import app, db
from models import Student

with app.app_context():
    # Add sample students
    student1 = Student(nim="12345", nama="John Doe", program_studi="Teknik", status="active")
    student2 = Student(nim="12346", nama="Jane Smith", program_studi="Ekonomi", status="active")

    db.session.add(student1)
    db.session.add(student2)
    db.session.commit()
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `app.run(port=5001)`
2. **Database errors**: Delete `billing.db` and restart the application
3. **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`

### Logs

Check the console output for detailed error messages and scheduler activity.

## Production Deployment

For production deployment:

1. Set `FLASK_ENV=production` in `.env`
2. Use a production WSGI server like Gunicorn
3. Configure a production database (PostgreSQL recommended)
4. Set up proper logging and monitoring
5. Configure webhook secrets securely

## License

This project is for educational purposes.
