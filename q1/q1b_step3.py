import boto3

# Create an SQS client
sqs_client = boto3.client('sqs')

# Specify the name of the queue
queue_name = 'a2q1-queue'

# Get the URL of the queue
queue_url_response = sqs_client.get_queue_url(QueueName=queue_name)
queue_url = queue_url_response['QueueUrl']

# Get the queue ARN using the queue URL
queue_attributes_response = sqs_client.get_queue_attributes(
    QueueUrl=queue_url,
    AttributeNames=['QueueArn']
)
queue_arn = queue_attributes_response['Attributes']['QueueArn']

sqs_client.set_queue_attributes(
    QueueUrl=queue_url,
    Attributes={'VisibilityTimeout': '1800'}
)

# Create a Lambda client
lambda_client = boto3.client('lambda')

response = lambda_client.create_event_source_mapping(
    FunctionName='a2q1_lambda',
    EventSourceArn=queue_arn,
    Enabled=True,
    BatchSize=10
)