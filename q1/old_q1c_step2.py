import boto3

aws_lambda = boto3.client('lambda')
iam_client = boto3.client('iam')

role = iam_client.get_role(RoleName='LabRole')

# Initialize S3 client
s3_client = boto3.client('s3')

# Define the bucket name (must be globally unique)
bucket_name = 'a2q1-bucket'

# Create the S3 bucket
s3_client.create_bucket(Bucket=bucket_name)
print(f"S3 bucket {bucket_name} created successfully.")

# Initialize a DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Define the table name
table_name = 'a2q1-table'

# Create the DynamoDB table
table = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
        {'AttributeName': 'user_id', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}  # Sort key
    ],
    AttributeDefinitions=[
        {'AttributeName': 'user_id', 'AttributeType': 'S'},
        {'AttributeName': 'timestamp', 'AttributeType': 'S'}
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
)
table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
print(f"DynamoDB table {table_name} created successfully.")


with open('q1c_lambda.zip', 'rb') as f:
    lambda_zip = f.read()

try:
    response = aws_lambda.create_function(
        FunctionName='a2q1_lambda',
        Runtime='python3.11',
        Role=role['Role']['Arn'],
        Handler='q1c_lambda.lambda_handler',
        Code=dict(ZipFile=lambda_zip),
        Timeout=300
)
except aws_lambda.exceptions.ResourceConflictException:
    response = aws_lambda.update_function_code(
        FunctionName='a2q1_lambda',
        ZipFile=lambda_zip
        )