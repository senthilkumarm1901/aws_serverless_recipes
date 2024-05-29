## Project Title:
- `How to create a python AWS Lambda with API endpoint via SAM`

### Query 1:

```
Hi which model do you use?
'''
I use the GPT-4 version of OpenAI's GPT models
'''
```

### Query 2: 

```
Create a Python code that accepts a text and a regex pattern and returns the matched string portion. Return "No Match" if there is no match for that pattern in that text

The code should be compatible to run in AWS Lambda. 

Ensure the event dictionary is of the below format.

{
    "text": "Hello, my name is Senthil Kumar. I work as a software engineer at XYZ. my email id is senthil_kumar@gmail.com. Reach me at mobile +91 9876541230",
    "regex_pattern": "(\w+)[-_.]?(\w+)@((\w|-)+)\.\w+"
}

'''
import re
import json

def lambda_handler(event, context):
    text = event['text']
    pattern = event['regex_pattern']

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
'''
```

### Query 3: 

```
I want to deploy the above code in AWS Lambda Function with an API Gateway attached. 

Provide me a SAM Template that does the following. 
- Create IAM Role and Policy
- Create a Lambda function with the above IAM Role and Policy and below config

FUNCTION_NAME="simple_regex_lambda"
MEMORY_SIZE=256
TIMEOUT=30
ARCHITECTURE=arm64

- Create a AWS API Gateway Service that is integrated to the Lambda Function

'''
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: An AWS Serverless Specification template describing your function.
Resources:
  SimpleRegexLambdaRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service:
                - lambda.amazonaws.com
            Action:
              - sts:AssumeRole
      Policies:
        - PolicyName: SimpleRegexLambdaPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - logs:CreateLogGroup
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                Resource: '*'

  SimpleRegexLambda:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: simple_regex_lambda
      Handler: lambda_handler.lambda_handler
      Runtime: python3.8
      MemorySize: 256
      Timeout: 30
      Architecture: arm64
      Role: !GetAtt SimpleRegexLambdaRole.Arn
      Events:
        SimpleRegexApi:
          Type: Api
          Properties:
            Path: /test
            Method: post

Outputs:
  SimpleRegexApi:
    Description: "API Gateway endpoint URL for Prod environment"
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/test/"
'''
```

### Query 4:

```
How is ${ServerlessRestApi} value replaced? Also, I want the API gateway path to have the same name as the lambda function

'''
The ${ServerlessRestApi} is a CloudFormation intrinsic variable that AWS SAM automatically generates when you define an AWS::Serverless::Function with an event of type Api. It refers to the logical ID of the API Gateway RestApi resource that is created by AWS SAM.

To have the API Gateway path the same as the Lambda function name, you can modify the Path property under Events in the SAM template. Here's how you can do it:


Events:
  SimpleRegexApi:
    Type: Api
    Properties:
      Path: /simple_regex_lambda
      Method: post
'''

```

### Query 5:

```
Should the Method be post or put in the API Gateway? We are passing two parameters text and regex_pattern to the lambda. I want them to be passed them in query in the API.

'''
If you want to pass parameters via the query string, then you should use the GET method. The POST and PUT methods are typically used when you want to send data in the body of the request, not in the query string.

Here's how you can modify the Method property under Events in the SAM template:

Events:
  SimpleRegexApi:
    Type: Api
    Properties:
      Path: /simple_regex_lambda
      Method: get

Now, the API Gateway will have a GET method at the /simple_regex_lambda path. You can pass parameters to the Lambda function via the query string like this: /simple_regex_lambda?text=your_text&regex_pattern=your_pattern.   
'''
```

### Query 6: 

```
If the API pattern is like /simple_regex_lambda?text=your_text&regex_pattern=your_pattern , how should the event in lambda_function.lambda_handler(event,context) be read inside the lambda function

'''
When you pass parameters via the query string in an API Gateway request, they are included in the event dictionary that is passed to the Lambda function. They are located under the queryStringParameters key.

Here is how you can modify the lambda_handler function to read the text and regex_pattern parameters from the event dictionary:

import re

def lambda_handler(event, context):
    parameters = event['queryStringParameters']
    text = parameters['text']
    regex_pattern = parameters['regex_pattern']
    
    match = re.search(regex_pattern, text)
    
    if match:
        return match.group()
    else:
        return "No Match"


This function extracts the text and regex_pattern parameters from the queryStringParameters key of the event dictionary. It then uses these parameters to perform the regex search.
'''
```


### Query 7: 

```
Is it possible to add a simple custom password protection while invoking the API gateway url. I need a simplest authorizer possible.Is it possible to include that in the SAM template ?

'''
Yes, you can add a simple Lambda authorizer to your API Gateway for basic password protection. This authorizer will be a separate Lambda function that checks the password provided in the headers of the API request.

Here's how you can modify the SAM template to include a Lambda authorizer:

AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: An AWS Serverless Specification template describing your function.
Resources:
  SimpleRegexLambdaRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service:
                - lambda.amazonaws.com
            Action:
              - sts:AssumeRole
      Policies:
        - PolicyName: SimpleRegexLambdaPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - logs:CreateLogGroup
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                Resource: '*'

  SimpleRegexLambda:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: simple_regex_lambda
      Handler: lambda_handler.lambda_handler
      Runtime: python3.8
      MemorySize: 256
      Timeout: 30
      Architecture: arm64
      Role: !GetAtt SimpleRegexLambdaRole.Arn
      Events:
        SimpleRegexApi:
          Type: Api
          Properties:
            Path: /simple_regex_lambda
            Method: get
            Auth:
              Authorizer: SimpleRegexLambdaAuthorizer

  SimpleRegexLambdaAuthorizer:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: simple_regex_lambda_authorizer
      Handler: authorizer_handler.lambda_handler
      Runtime: python3.8
      MemorySize: 128
      Timeout: 3
      Role: !GetAtt SimpleRegexLambdaRole.Arn

Outputs:
  SimpleRegexApi:
    Description: "API Gateway endpoint URL for Prod environment"
    Value: !Sub "https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/simple_regex_lambda/"

In this template, SimpleRegexLambdaAuthorizer is a new Lambda function that serves as the authorizer. You need to replace authorizer_handler.lambda_handler with the correct path to your authorizer function.

The authorizer function should look something like this:

def lambda_handler(event, context):
    token = event['headers']['Authorization']
    if token == 'your_password':
        return generate_policy('user', 'Allow', event['methodArn'])
    else:
        return generate_policy('user', 'Deny', event['methodArn'])

def generate_policy(principal_id, effect, resource):
    return {
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
'''
```

### Query 8:

```
I have saved the SimpleRegexLambdaAuthorizer as authorizer_handler.py and the SAM template as template.yaml.

Can you access them in simple_python_lambda_via_sam_copilot_attempt folder? Are they looking correct?

'''
I'm sorry for any confusion, but as an AI developed by OpenAI, I don't have the ability to access your local file system or any external servers to view or retrieve files. I can only provide assistance based on the information you provide to me directly during our conversation.

However, if you share the content of the files here, I'd be more than happy to review them for you.
'''
```

### Query 9:

```
Ok, I have selected template.yaml file in the adjacent window. Can you review it?

'''
The template.yaml file you've provided looks correct based on your requirements. It defines an AWS SAM template that:

Creates an IAM role (SimpleRegexLambdaRole) with a policy that allows the role to create and write to CloudWatch Logs.
Defines a Lambda function (SimpleRegexLambda) with the specified properties (function name, handler, runtime, memory size, timeout, architecture, and role). The function is associated with an API Gateway event trigger.
The API Gateway event trigger is configured with a GET method at the /simple_regex_lambda path and uses a Lambda authorizer (SimpleRegexLambdaAuthorizer).
Defines the Lambda authorizer function (SimpleRegexLambdaAuthorizer) with the specified properties (function name, handler, runtime, memory size, timeout, and role).
Outputs the API Gateway endpoint URL for the Prod environment.
Please ensure that the handlers (lambda_handler.lambda_handler and authorizer_handler.lambda_handler) correctly point to your Python files and functions. The format is file_name.function_name.

Also, remember to replace 'your_password' in the authorizer function with your actual password.
'''
```

### Query 10:

```
Now, check authorizer_handler.py that is selected

'''
The authorizer_handler.py code you've provided looks correct. It defines a Lambda function that:

Extracts the Authorization header from the incoming event.
If the Authorization header matches 'your_password', it generates an IAM policy that allows the request.
If the Authorization header does not match 'your_password', it generates an IAM policy that denies the request.
The generate_policy function correctly creates an IAM policy with the provided principal ID, effect (Allow or Deny), and resource.

Please remember to replace 'your_password' with your actual password.
'''
```

### Query 11:

```
Give me the SAM command to deploy the final template.yaml file. Allow me to explicitly pass AWS_ACCOUNT_ID and REGION (I may want to deploy it multiple regions or accounts).

'''
To deploy your AWS SAM application, you can use the sam deploy command. Here's an example command that allows you to explicitly pass the AWS account ID and region:

AWS_ACCOUNT_ID=your_account_id
REGION=your_region
STACK_NAME=your_stack_name
S3_BUCKET=your_s3_bucket

sam build --use-container

sam package \
  --output-template-file packaged.yaml \
  --s3-bucket $S3_BUCKET \
  --region $REGION

sam deploy \
  --template-file packaged.yaml \
  --stack-name $STACK_NAME \
  --capabilities CAPABILITY_IAM \
  --region $REGION
'''

Replace your_account_id, your_region, your_stack_name, and your_s3_bucket with your actual AWS account ID, the region where you want to deploy the application, the name you want to give to the CloudFormation stack, and the S3 bucket where you want to upload your application code, respectively.

The sam build command builds your application and prepares it for deployment. The sam package command uploads your application code to an S3 bucket and produces a packaged AWS SAM template. The sam deploy command deploys your application using the packaged template.

Please ensure that you have the necessary permissions to perform these operations in the specified AWS account and region.
```

### Query 12: 

```
What is the use of sam package for simple lambda_function.py ? Can I avoid uploading the code to S3 and directly deploy in to the lambda function? Or is this a best practice?

'''
The sam package command is used to package an AWS SAM application. It creates a .zip file of your code and dependencies, and uploads them to an S3 bucket. It also returns a copy of your AWS SAM template, replacing references to local artifacts with the Amazon S3 location where the command uploaded the artifacts.

For simple Lambda functions, you might not need to use the sam package command. You can use the AWS CLI's aws lambda update-function-code command to upload your code directly from your local machine to the Lambda function.

However, using sam package and sam deploy is considered a best practice for a few reasons:

Consistency: Whether your application is simple or complex, the process to package and deploy it remains the same. This can make it easier to manage and automate deployments.

Versioning: When you upload your code to an S3 bucket, you have a centralized place to manage and version your code. This can make it easier to roll back deployments, share code across multiple environments, and track changes over time.

Integration with AWS SAM and AWS CloudFormation: The sam package and sam deploy commands are designed to work seamlessly with AWS SAM and AWS CloudFormation. This means you can define your application's resources, permissions, and event sources in a single AWS SAM template, and AWS SAM will handle the rest.

Large applications: If your application's deployment package is larger than 50 MB, you must upload it to an S3 bucket. The sam package command handles this for you.

So, while it's possible to avoid using sam package for simple applications, it's generally a good idea to use it for the reasons listed above.
'''
```

### Query 13:

```
Are both lambda_function.py and authorizer_handler.py packaged in the sam package command?

'''
Yes, the sam package command packages all the AWS Lambda functions defined in your AWS SAM template, including their code and any dependencies.

In your case, if both lambda_function.py and authorizer_handler.py are referenced in your template.yaml file as handlers for different AWS Lambda functions, then both will be included in the package that sam package creates.

The command zips up each function's code and dependencies separately, uploads them to the specified S3 bucket, and then modifies the template to point to the new location of the code in S3. This packaged template is what you then deploy with the sam deploy command.
'''
```

### Query 14: 

```
I have selected the template.yaml file and I am giving below the all the files inside the current directory. Is everything needed for the template.yaml present in this folder?

simple_python_lambda_via_sam_copilot_attempt 
├── authorizer_handler.py 
├── copilot_interactions.md 
├── lambda_function.py 
└── template.yaml

'''
Based on the template.yaml file and the directory structure you've provided, it seems like you have all the necessary files for your AWS SAM application.

Here's a breakdown:

template.yaml: This is your AWS SAM template that describes your serverless application.

authorizer_handler.py: This is the Python file that contains the code for your Lambda authorizer function. In your template.yaml, this is referenced in the Handler property of the SimpleRegexLambdaAuthorizer resource.

lambda_function.py: This is the Python file that contains the code for your main Lambda function. In your template.yaml, this is referenced in the Handler property of the SimpleRegexLambda resource.

copilot_interactions.md: This file doesn't seem to be directly related to your AWS SAM application. It might contain documentation or notes.

So, it looks like you have everything you need to package and deploy your AWS SAM application. Make sure that the lambda_handler function is defined in both authorizer_handler.py and lambda_function.py, as these are the entry points for your Lambda functions.
'''
```

### Query 15:

```
what does sam build --use-container do?

'''
The sam build --use-container command is used to build your AWS Serverless Application Model (SAM) application.

Here's what it does:

It creates a deployment package of your application's code and any dependencies. The deployment package is a .zip file that contains your code and any dependencies. The deployment package is what AWS Lambda uses to run your application.

The --use-container option tells SAM to build your application inside a Docker container. This can be useful if your application has native dependencies that need to be compiled on the same type of operating system as the one where your Lambda function will run. By using a Docker container, you can ensure that your application is built in an environment that's similar to the AWS Lambda environment.

The command creates a new directory, .aws-sam/build, where it places the deployment packages and updated AWS SAM template.

So, in summary, sam build --use-container prepares your AWS SAM application for deployment by creating deployment packages of your code and dependencies. It does this inside a Docker container to ensure compatibility with the AWS Lambda environment.
'''
```


### Query 16: 

```
To invoke your AWS SAM application locally, you can use the sam local start-api command. This command starts a local instance of API Gateway and invokes your Lambda function when you send a request to the local endpoint.

'''
Here's how you can start your local API:

sam build --use-container
sam local start-api

Once your local API is running, you can use curl to send a request to it. Assuming your API has a GET method at the /simple_regex_lambda path, here's how you can send a request:

curl http://127.0.0.1:3000/simple_regex_lambda

Please note that you need Docker running on your machine to use sam local start-api, as it runs your Lambda function inside a Docker container that replicates the AWS Lambda environment.

Also, if your Lambda function requires an Authorization header, you can include it in your curl command like this:

curl -H "Authorization: your_password" http://127.0.0.1:3000/simple_regex_lambda
'''
```

### Query 17:

```
Can you provide me the complete curl command where I upload a test_event.json like below. The authorization password is out_test_password

{
    "text": "Hello, my name is Senthil Kumar. I work as a software engineer at XYZ. my email id is senthil_kumar@gmail.com. Reach me at mobile +91 9876541230",
    "regex_pattern": "(\w+)[-_.]?(\w+)@((\w|-)+)\.\w+"
}

'''
Sure, you can use the curl command with the -d option to send a POST request with the JSON data in test_event.json. Assuming your local API has a POST method at the /simple_regex_lambda path, here's how you can send a request:


curl -X POST -H "Content-Type: application/json" -H "Authorization: out_test_password" -d @test_event.json http://127.0.0.1:3000/simple_regex_lambda

This command does the following:

-X POST specifies that this is a POST request.
-H "Content-Type: application/json" sets the Content-Type header to application/json, indicating that the request body contains JSON data.
-H "Authorization: out_test_password" sets the Authorization header to out_test_password.
-d @test_event.json sends the data in test_event.json as the request body.
http://127.0.0.1:3000/simple_regex_lambda is the URL of your local API.
Please replace test_event.json with the actual path to your JSON file if it's not in the same directory where you're running the curl command. Also, make sure your local API is running by executing the sam local start-api command.
'''
```

### Query 18:

```
How will this command work? 

curl -X POST -H "Content-Type: application/json" -H "Authorization: out_test_password" -d @test_event.json http://127.0.0.1:3000/simple_regex_lambda

I am expecting some thing like below inside the lambda_function.py 

def lambda_handler(event, context):
    parameters = event['queryStringParameters']
    text = parameters['text']
    regex_pattern = parameters['regex_pattern']

'''
The curl command you provided sends a POST request to your local API with the JSON data in test_event.json as the request body. However, the lambda_handler function in your lambda_function.py file is expecting the text and regex_pattern parameters to be in the queryStringParameters field of the event object.

When you send a POST request, the data in the request body is typically available in the body field of the event object, not the queryStringParameters field. The queryStringParameters field is used for query string parameters in a GET request.

Here's how you can modify your lambda_handler function to handle a POST request:

import json

def lambda_handler(event, context):
    body = json.loads(event['body'])
    text = body['text']
    regex_pattern = body['regex_pattern']
    # rest of your code

In this modified version of the function, json.loads(event['body']) is used to parse the JSON data in the request body. Then, the text and regex_pattern parameters are extracted from the parsed JSON data.
'''
```

### Query 19: 

```
How to delete the above stack created via SAM deploy in AWS cloud

'''
To delete an AWS SAM application, you can use the AWS CLI to delete the CloudFormation stack that was created when you deployed your SAM application. Here's how you can do it:

Open your terminal.

Run the following command:

aws cloudformation delete-stack --stack-name mySAMstack

Replace mySAMstack with the name of your stack. This is the same name you used with the --stack-name option when you ran the sam deploy command.

This command deletes the stack and all the resources it created. Please note that this operation cannot be undone. Make sure you no longer need the resources in the stack before you delete it.
'''
```



### Query 20:

```
Starting Build inside a container

Error: [InvalidResourceException('SimpleRegexLambda', 'property Architecture not defined for resource of type AWS::Serverless::Function'), InvalidResourceException('SimpleRegexLambdaAuthorizer', 'property Architecture not defined for resource of type AWS::Serverless::Function')] ('SimpleRegexLambda', 'property Architecture not defined for resource of type AWS::Serverless::Function') ('SimpleRegexLambdaAuthorizer', 'property Architecture not defined for resource of type AWS::Serverless::Function')

'''
The error message indicates that the Architecture property is not recognized for the AWS::Serverless::Function resource type. This property is used to specify the instruction set architecture for the AWS Lambda function.

As of AWS SAM version 1.27.0, the Architecture property is supported and can be set to x86_64 or arm64. If you're using an older version of AWS SAM, this property is not supported and you'll get an error if you try to use it.

You can check your AWS SAM version by running sam --version in your terminal. If you're using an older version, you can update AWS SAM with the following command:

After updating AWS SAM, try running sam build --use-container again. If you're still getting the error, please remove the Architecture property from your AWS SAM template if you don't need to use the arm64 architecture. If you need to use the arm64 architecture, make sure you're using AWS SAM version 1.27.0 or later.

'''
```

> The above was an error from CoPilot. 
> There was a problem in `Architectures` section in the `template.yaml` file (incorrectly mentioned as `Architecture` in the template)


### Query 21:

```
I keep getting json decode error.

[ERROR] JSONDecodeError: Invalid \escape: line 1 column 204 (char 203)

body = json.loads(event['body'])

The input json looks like this:

{ "text": "Hello, my name is Senthil Kumar. I work as a software engineer at XYZ. my email id is senthil_kumar@gmail.com. Reach me at mobile +91 9876541230", "regex_pattern": "(\w+)[-_.]?(\w+)@((\w|-)+).\w+" }

'''
The issue you're encountering is due to the backslashes in your regular expression. In JSON, the backslash (\) is an escape character, which means it's used to introduce special character sequences. If you want to include an actual backslash in your JSON data, you need to escape it by using two backslashes (\\).

Here's how your JSON data should look:
{
    "text": "Hello, my name is Senthil Kumar. I work as a software engineer at XYZ. my email id is senthil_kumar@gmail.com. Reach me at mobile +91 9876541230",
    "regex_pattern": "(\\w+)[-_.]?(\\w+)@((\\w|-)+)\\.\\w+"
}

In this version of the JSON data, each backslash in the regular expression is escaped with another backslash. This should resolve the JSONDecodeError you're getting.
'''
```

> Helped me solve the error in my `test_event.json`


### Query 22:

```
When I did

sam deploy --template-file packaged.yaml --stack-name $STACK_NAME --capabilities CAPABILITY_IAM --region $REGION

I got the below error. How to rectify the template.yaml that is selected

Error: Failed to create changeset for the stack: regex-lambda-with-api-copilot, ex: Waiter ChangeSetCreateComplete failed: Waiter encountered a terminal failure state: For expression "Status" we matched expected path: "FAILED" Status: FAILED. Reason: Transform AWS::Serverless-2016-10-31 failed with: Invalid Serverless Application Specification document. Number of errors found: 1. Resource with id [SimpleRegexLambda] is invalid. Event with id [SimpleRegexApi] is invalid. Unable to set Authorizer [SimpleRegexLambdaAuthorizer] on API method [post] for path [/simple_regex_lambda] because the related API does not define any Authorizers.

The error message indicates that the SimpleRegexApi event in the SimpleRegexLambda function is trying to use an authorizer (SimpleRegexLambdaAuthorizer), but the related API does not define any authorizers.

In AWS SAM, authorizers are defined at the AWS::Serverless::Api level, not at the individual event level within a AWS::Serverless::Function.

To fix this issue, you need to define an AWS::Serverless::Api resource in your template and specify the authorizer there. Here's an example:


The SimpleRegexApi should be a separate resource at the same level as SimpleRegexLambda, not nested under it. Here's an example of how your AWS SAM template should look:

'''
Resources:
  SimpleRegexLambda:
    Type: AWS::Serverless::Function
    Properties:
      # ...

  SimpleRegexLambdaAuthorizer:
    Type: AWS::Serverless::Function
    Properties:
      # ...

  SimpleRegexApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: Prod
      Auth:
        DefaultAuthorizer: SimpleRegexLambdaAuthorizer
        Authorizers:
          SimpleRegexLambdaAuthorizer:
            FunctionArn: !GetAtt SimpleRegexLambdaAuthorizer.Arn
      DefinitionBody:
        paths:
          /simple_regex_lambda:
            post:
              x-amazon-apigateway-integration:
                httpMethod: POST
                type: aws_proxy
                uri: 
                  Fn::Sub: arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${SimpleRegexLambda.Arn}/invocations
'''
In this example, SimpleRegexLambda, SimpleRegexLambdaAuthorizer, and SimpleRegexApi are all separate resources defined at the same level under the Resources section of the AWS SAM template.

Please replace the # ... with the actual properties for your Lambda functions and API.

After updating your AWS SAM template, try running the sam deploy command again. If you're still getting the error, please check your AWS SAM template for any syntax errors or unsupported properties.
```

### Query 23: 

```
When I did sam validate I got the below error for the selected template.yaml file

Error: [InvalidResourceException('SimpleRegexApi', "Unable to add Auth configuration because 'DefinitionBody' does not contain a valid Swagger definition.")] ('SimpleRegexApi', "Unable to add Auth configuration because 'DefinitionBody' does not contain a valid Swagger definition.")

'''
The error message indicates that the DefinitionBody of the SimpleRegexApi resource does not contain a valid Swagger (OpenAPI) definition. The DefinitionBody is where you define your API's resources and methods.

In your current DefinitionBody, you're missing the swagger or openapi version field, and the info and paths fields are not properly nested under the root of the definition.

Here's how you can fix your DefinitionBody:

SimpleRegexApi:
  Type: AWS::Serverless::Api
  Properties:
    StageName: Prod
    Auth:
      DefaultAuthorizer: SimpleRegexLambdaAuthorizer
      Authorizers:
        SimpleRegexLambdaAuthorizer:
          FunctionArn: !GetAtt SimpleRegexLambdaAuthorizer.Arn
    DefinitionBody:
      swagger: '2.0'
      info:
        title: SimpleRegexApi
      paths:
        /simple_regex_lambda:
          post:
            x-amazon-apigateway-integration:
              httpMethod: POST
              type: aws_proxy
              uri: 
                Fn::Sub: arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${SimpleRegexLambda.Arn}/invocations

'''
In this updated version, the DefinitionBody now contains a valid Swagger definition. It specifies the Swagger version (2.0), provides an info object with a title, and properly nests the paths under the root of the definition.

After updating your AWS SAM template, try running the sam validate command again. If you're still getting the error, please check your AWS SAM template for any syntax errors or unsupported properties.
```

### Query 24:

```
Invoking the APIGW_URL like below command, resulted in the below error

command: curl -X POST -H "Content-Type: application/json" -H "Authorization: out_test_password" -d @test_event.json ${APIGW_URL}

error: KeyError: 'headers'

Infact the event to the authorizer does not seem to have headers.

{'type': 'TOKEN', 'methodArn': 'arn:aws:execute-api:ap-south-1::/Prod/POST/simple_regex_lambda/', 'authorizationToken': 'out_test_password'}

'''

'''

```

### Query 25:

```
In the AWS API Gateway console, enabled cloudwatch logs to the api `SimpleRegexApi` and found out the below error

(d0f70f44-e843-42ff-b628-28384d82a707) Sending request to https://lambda.<REGION>.amazonaws.com/2015-03-31/functions/arn:aws:lambda:<REGION>:<ACCOUNT_ID>:function:simple_regex_lambda/invocations

(d0f70f44-e843-42ff-b628-28384d82a707) Execution failed due to configuration error: Invalid permissions on Lambda function. 

I have selected my template.yaml,can you rectify it

'''
The SimpleRegexLambdaInvokePermission resource has to be added to give API Gateway and it has the necessary permissions to invoke your SimpleRegexLambda function.

Resources:
  ....
  SimpleRegexLambdaInvokePermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !GetAtt SimpleRegexLambda.Arn
      Action: lambda:InvokeFunction
      Principal: apigateway.amazonaws.com
'''
```

> This above suggestion fixed the error. 

### Query 26:

```
Using aws cli command how to delete my stack

'''
aws cloudformation delete-stack --stack-name ${STACK_NAME}
'''
```