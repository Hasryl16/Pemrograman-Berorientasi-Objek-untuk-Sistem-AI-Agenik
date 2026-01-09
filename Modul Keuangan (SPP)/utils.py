import csv
import json
from collections import defaultdict

def analyze_payment_data(csv_path):
    """
    Analyze payment data from CSV file and generate insights.

    Args:
        csv_path (str): Path to the CSV file containing payment data

    Returns:
        dict: JSON-serializable dictionary with analysis results
    """
    try:
        payments = []
        total_revenue = 0
        collection_count = 0
        total_count = 0
        debtors = defaultdict(float)

        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                nim = row['nim']
                jumlah = float(row['jumlah'])
                status = row['status'].lower()

                payments.append({
                    'nim': nim,
                    'jumlah': jumlah,
                    'tanggal': row['tanggal'],
                    'status': status
                })

                total_revenue += jumlah
                total_count += 1

                if status == 'lunas':
                    collection_count += 1
                elif status == 'partial':
                    debtors[nim] += jumlah

        # Calculate collection rate
        collection_rate = (collection_count / total_count) * 100 if total_count > 0 else 0

        # Get top 10 debtors (those with partial payments)
        top_debtors = sorted(debtors.items(), key=lambda x: x[1], reverse=True)[:10]
        top_debtors_list = [{'nim': nim, 'outstanding_amount': amount} for nim, amount in top_debtors]

        result = {
            'total_revenue': total_revenue,
            'collection_rate': round(collection_rate, 2),
            'total_payments': total_count,
            'collected_payments': collection_count,
            'top_10_debtors': top_debtors_list,
            'payments': payments
        }

        return json.dumps(result, indent=2, default=str)

    except Exception as e:
        raise Exception(f"Error analyzing payment data: {str(e)}")
