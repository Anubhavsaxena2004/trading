import boto3
import json
from lambda_handler import lambda_handler
import os
def api_gateway_handler(event, context):
    # Extract date from query parameters
    query_params = event.get('queryStringParameters', {})
    date = query_params.get('date')
    
    # Call lambda handler with date
    lambda_event = {'date': date} if date else {}
    result = lambda_handler(lambda_event, context)
    
    # Return formatted response for API Gateway
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'message': 'Analysis completed successfully',
            'date': date or 'today'
        })
    }