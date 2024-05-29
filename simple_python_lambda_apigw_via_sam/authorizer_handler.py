def lambda_handler(event, context):
    print(event)
    try:
        # when running locally
        token = event['headers']['Authorization']
    except: 
        # when running in AWS
        token = event['authorizationToken']
    print(token)
    if token == 'our_test_password':
        return generate_policy('user', 'Allow', event['methodArn'])
    else:
        return generate_policy('user', 'Deny', event['methodArn'])

def generate_policy(principal_id, effect, resource):
    policy = {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': resource
            }]
        }
    }
    print(policy)
    return policy