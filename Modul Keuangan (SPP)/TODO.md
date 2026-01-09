- [ ] Create requirements.txt with dependencies
- [ ] Create config.py for configuration
- [ ] Create run.py to start the application

## Database Models
- [ ] Create models.py with Student, Billing, Payment models
- [ ] Set up SQLAlchemy database connection

## Billing Service
- [ ] Implement generate_billing function in services.py
- [ ] Create billing generation logic (semester start, amounts by program)
- [ ] Set due dates (2 weeks after semester start)

## Scheduler
- [ ] Create scheduler.py with APScheduler setup
- [ ] Configure cron job to run at semester start

## Payment Processing
- [ ] Implement process_payment function in services.py
- [ ] Handle payment status updates (unpaid -> partial -> paid)
- [ ] Create payment records
- [ ] Use database transactions for atomicity

## Webhook Handler
- [ ] Implement handle_webhook function in services.py
- [ ] Add signature verification for security
- [ ] Extract transaction data and call process_payment
- [ ] Return 200 OK response

## Data Analysis
- [ ] Create analyze_payment_data function in utils.py
- [ ] Process CSV input with nim, jumlah, tanggal, status
- [ ] Generate insights: total revenue, collection rate, top 10 debtors
- [ ] Output JSON format for dashboard

## Main Application
- [ ] Create app.py with Flask routes
- [ ] Set up database initialization
- [ ] Integrate scheduler startup
- [ ] Add API endpoints for billing and payment operations

## Testing
- [ ] Test billing generation
- [ ] Test payment processing
- [ ] Test webhook handling
- [ ] Test data analysis
=======
## Project Setup
- [x] Create requirements.txt with dependencies
- [x] Create config.py for configuration
- [x] Create run.py to start the application

## Database Models
- [x] Create models.py with Student, Billing, Payment models
- [x] Set up SQLAlchemy database connection

## Billing Service
- [x] Implement generate_billing function in services.py
- [x] Create billing generation logic (semester start, amounts by program)
- [x] Set due dates (2 weeks after semester start)

## Scheduler
- [x] Create scheduler.py with APScheduler setup
- [x] Configure cron job to run at semester start

## Payment Processing
- [x] Implement process_payment function in services.py
- [x] Handle payment status updates (unpaid -> partial -> paid)
- [x] Create payment records
- [x] Use database transactions for atomicity

## Webhook Handler
- [x] Implement handle_webhook function in services.py
- [x] Add signature verification for security
- [x] Extract transaction data and call process_payment
- [x] Return 200 OK response

## Data Analysis
- [x] Create analyze_payment_data function in utils.py
- [x] Process CSV input with nim, jumlah, tanggal, status
- [x] Generate insights: total revenue, collection rate, top 10 debtors
- [x] Output JSON format for dashboard

## Main Application
- [x] Create app.py with Flask routes
- [x] Set up database initialization
- [x] Integrate scheduler startup
- [x] Add API endpoints for billing and payment operations

## Testing
- [ ] Test billing generation
- [ ] Test payment processing
- [ ] Test webhook handling
- [ ] Test data analysis
