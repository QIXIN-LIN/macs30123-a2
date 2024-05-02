import json
import boto3

def send_survey(survey_path, sqs_url):
    '''
        Input:
            survey_path (str): path to JSON survey data (e.g. ‘./survey.json’)
            sqs_url (str): URL for SQS queue
        Output:
            StatusCode (int): indicating whether the survey was successfully 
            sent into the SQS queue (200) or not (0)
    '''
    # Load survey data from the file
    with open(survey_path, 'r') as file:
        survey_data = json.load(file)

    # Create a boto3 client for SQS
    sqs_client = boto3.client('sqs')

    # Send the message to the SQS queue
    try:
        response = sqs_client.send_message(
            QueueUrl=sqs_url,
            MessageBody=json.dumps(survey_data)
        )
        return 200  # Successful status code
    except Exception as e:
        print(f"Failed to send message: {e}")
        return 0  # Failure status code
