import os
import io
import boto3
import json
import csv

# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    
    try:
        data = json.loads(event["body"])
    except:
        data = event["body"]
    payload = data['data']
    print(payload)
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='application/json',
                                       Body=json.dumps(payload))
    print(response)
    result = json.loads(response['Body'].read().decode())
    
    return {
        'statusCode': 200,
        "headers" : {
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
        }, 
        'body': json.dumps({'result': result}) 
    }