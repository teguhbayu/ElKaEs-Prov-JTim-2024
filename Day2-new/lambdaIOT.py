import boto3 
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('sensor')

def lambda_handler (event, context):
    process_and_save_data(event)

def process_and_save_data(payload):
    try:
        payload['temperature'] = Decimal(str(payload['temperature']))
        payload['humidity'] = Decimal(str(payload['humidity']))
        payload['gas_concentration'] = Decimal(str(payload['gas_concentration']))
        payload['fire_intensity'] = Decimal(str(payload['fire_intensity']))

        response = table.put_item(Item=payload)
        print(f'Data Success: {response}')
        return{
            'statusCode': 200,
            'body': 'Data Success'
        }
    except:
        return{
            'statusCode': 500,
            'body': 'Data Error'
        }