import boto3
import csv
from io import StringIO
import os

s3 = boto3.client('s3')
BUCKET_NAME = 'my-trading-data'  # Replace with your bucket name

def lambda_handler(event, context):
    date = event.get('date')  # e.g., "2025-06-04"
    if not date:
        return {"statusCode": 400, "body": "Missing date parameter"}

    year, month, day = date.split('-')
    key = f"{year}/{month}/{day}/trades.csv"

    try:
        # Fetch file from S3
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        lines = obj['Body'].read().decode('utf-8').splitlines()
        reader = csv.DictReader(lines)

        stats = {}
        for row in reader:
            stock = row['stock']
            volume = int(row['volume'])
            price = float(row['price'])
            if stock not in stats:
                stats[stock] = {'total_volume': 0, 'total_value': 0.0}
            stats[stock]['total_volume'] += volume
            stats[stock]['total_value'] += price * volume

        # Prepare analysis CSV content
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['stock', 'total_volume', 'average_price'])

        for stock, data in stats.items():
            avg_price = round(data['total_value'] / data['total_volume'], 2)
            writer.writerow([stock, data['total_volume'], avg_price])

        # Save analysis file to S3
        output_key = f"{year}/{month}/{day}/analysis_{date}.csv"
        s3.put_object(Bucket=BUCKET_NAME, Key=output_key, Body=output.getvalue())

        return {
            'statusCode': 200,
            'message': f"Analysis saved to {output_key}"
        }

    except Exception as e:
        return {"statusCode": 500, "error": str(e)}
