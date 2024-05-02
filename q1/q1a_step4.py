import boto3
from q1a_func import send_survey
import os


# Create an SQS client
sqs_client = boto3.client('sqs')

# Specify the name of your queue
queue_name = 'a2q1-queue'

# Get the URL of the queue
queue_url_response = sqs_client.get_queue_url(QueueName=queue_name)
sqs_url = queue_url_response['QueueUrl']

json_directory = './test_json'


# Iterate over each file in the directory and send it to the SQS queue
for filename in os.listdir(json_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(json_directory, filename)
        status_code = send_survey(file_path, sqs_url)
        print(f"File: {filename}, Status Code: {status_code}")

# This script will need to be run in an environment with network access to AWS