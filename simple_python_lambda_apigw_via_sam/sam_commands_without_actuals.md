AWS_ACCOUNT_ID=your_account_id
REGION=your_region
STACK_NAME=your_stack_name
S3_BUCKET=your_s3_bucket

sam build --use-container
sam validate
sam local start-api

```bash
sam package \
  --output-template-file packaged.yaml \
  --s3-bucket $S3_BUCKET \
  --region $REGION

sam deploy \
  --template-file packaged.yaml \
  --stack-name $STACK_NAME \
  --capabilities CAPABILITY_IAM \
  --region $REGION
```


## Result:
- When running `sam local start-api`

```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: out_test_password" -d @test_event.json http://127.0.0.1:3000/simple_regex_lambda      

"senthil_kumar@gmail.com"
```

- After deploying in AWS cloud
```bash
APIGW_ID=<some_id>
APIGW_URL=https://${APIGW_ID}.execute-api.${REGION}.amazonaws.com/Prod/simple_regex_lambda/ 

curl -X POST -H "Content-Type: application/json" -H "Authorization: out_test_password" -d @test_event.json ${APIGW_URL}
"senthil_kumar@gmail.com"

```