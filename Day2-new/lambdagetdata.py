import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table_name = 'sensor'

def lambda_handler(event,context):
    http_method = event["httpMethod"]

    if http_method == 'GET':
        return get_items_from_dynamodb()
    
    else:
        return{
            'statusCode': 405,
            'body': json.dumps("Method not allowed")
        }

def get_items_from_dynamodb():
    try:
        table = dynamodb.Table(table_name)
        response = table.scan()
        items = response['Items']

        for item in items:
            for key, value in item.items():
                if isinstance(value, decimal):
                    item[key] = float(value)
        return{
            'statusCode': 200,
            'body': json.dumps(items)
        }
    except Exception as e:
        return{
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
