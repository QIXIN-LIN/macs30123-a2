import boto3
import json
from datetime import datetime

# Initialize the S3 and DynamoDB clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # Validate the survey response
    for record in event['Records']:
        body = json.loads(record['body'])
        print("Processing record:", body)
        
        if int(body['time_elapsed']) > 3 and len(body['freetext']) != 0:
            # Store the survey in S3
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            file_name = f"{timestamp}_{body['user_id']}.json"
            s3.put_object(
                Bucket='a2q1-bucket',  # Add your S3 bucket name
                Key=file_name,
                Body=json.dumps(event).encode('utf-8')
            )
    
            table = dynamodb.Table('a2q1-table')
            
            # Check if the user already has an entry
            response = table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(body['user_id'])
            )
            # Calculate the new survey count
            survey_count = len(response['Items']) + 1  # Adding 1 for the current survey
                
            # DynamoDB item
            item = {
                'user_id': body['user_id'],
                'timestamp': timestamp,
                'time_elapsed': body['time_elapsed'],
                'q1': body['q1'],
                'q2': body['q2'],
                'q3': body['q3'],
                'q4': body['q4'],
                'q5': body['q5'],
                'freetext': body['freetext'],
                'survey_count': survey_count  # Updated count of surveys completed
            }
    
            table.put_item(Item=item)
            print("Valid response!")
        else:
            print("Invalid response!")
