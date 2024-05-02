import boto3


# Create an SQS client
sqs_client = boto3.client('sqs')

response = sqs_client.create_queue(
    QueueName='a2q1-queue'
)
print(response)