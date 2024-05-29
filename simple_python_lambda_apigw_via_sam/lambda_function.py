import re
import json

def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    text = body['text']
    regex_pattern = body['regex_pattern']
    # rest of your code

    match = re.search(regex_pattern, text)
    if match:
        return {
            'statusCode': 200,
            'body': json.dumps(match.group())
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps("No Match")
        }