import boto3

# Create an SQS client
sqs_client = boto3.client('sqs')

# Specify the name of your queue
queue_name = 'a2q1-queue'

# Get the URL of the queue
queue_url_response = sqs_client.get_queue_url(QueueName=queue_name)
sqs_url = queue_url_response['QueueUrl']


# Delete the SQS queue
response = sqs_client.delete_queue(QueueUrl=sqs_url)
print(response)

# Also delete S3 and DynamoDB manually