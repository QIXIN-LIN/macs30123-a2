import json
import boto3
from datetime import datetime
import os

# Initialize the S3 and DynamoDB clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Environment variables for S3 bucket and DynamoDB table names
s3_bucket = os.environ['a2q1-bucket']
dynamodb_table = os.environ['a2q1-table']

def lambda_handler(event, context):
    '''
    Test event: 
    {
    "user_id": "0001",
    "timestamp": "092821120000",
    "time_elapsed": 5,
    "q1": 5,
    "q2": 3,
    "q3": 2,
    "q4": 2,
    "q5": 4,
    "freetext": "I had a very bad day today..."
}
    '''
    # Assuming 'event' contains the survey data

    for record in event['Records']:
        # Parse the message body (survey data) from the SQS message
        survey_data = json.loads(record['body'])

        # Validate the survey response
        if int(survey_data['time_elapsed']) > 3 and survey_data['freetext'].strip() != '':
            # Store the survey in S3
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            file_name = f"{timestamp}_{survey_data['user_id']}.json"
            s3.put_object(Bucket=s3_bucket, Key=file_name, Body=json.dumps(survey_data))

            table = dynamodb.Table(dynamodb_table)
            table.put_item(
                Key={
                    'user_id': survey_data['user_id']
                },
                UpdateExpression="SET time_elapsed = :time_elapsed, q1 = :q1, q2 = :q2, q3 = :q3, q4 = :q4, q5 = :q5, "
                                "freetext = :freetext, survey_count = if_not_exists(survey_count, :start) + :inc",
                ExpressionAttributeValues={
                    ':time_elapsed': survey_data['time_elapsed'],
                    ':q1': survey_data['q1'],
                    ':q2': survey_data['q2'],
                    ':q3': survey_data['q3'],
                    ':q4': survey_data['q4'],
                    ':q5': survey_data['q5'],
                    ':freetext': survey_data['freetext'],
                    ':start': 0,
                    ':inc': 1
                },
                ReturnValues="UPDATED_NEW"
            )
        else:
            print("Invalid survey response")

# The lambda_handler would be triggered by the SQS messages
