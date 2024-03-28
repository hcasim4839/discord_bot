# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

import boto3
from botocore.exceptions import ClientError
import json
import requests
from dotenv import load_dotenv
import os
import datetime
import logging 

logger = logging.getLogger(__name__)
load_dotenv()

def get_secret(secret_key, secret_name):
    '''
    Connects to aws secret manager
        Returns:
            String

    '''
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret_dict = json.loads(get_secret_value_response['SecretString'])


    return secret_dict.get(secret_key)

def start_server(game_name):
    '''
    Connects to aws lambda function

        Returns:    
            A status code with json response otherise Exception class and exception message if exception occured
            
    '''
    try:
        url = 'https://q19me3z8id.execute-api.us-east-1.amazonaws.com/Prod/connect/Aternos'

        json_request = {
            "gameName": game_name
        }

        response = requests.post(url,json_request)
        print(f'The response from url:\n{response}')

        json_message = response.json()

        logger.info(f'Status code: {response.status_code}')
        print(f'JSON response: {json_message}')

        if response.status_code == 200:
            logger.info(f'Response successful')
            return response.status_code, json_message
        else:
            return response.status_code, json_message
    except Exception as e:
        exception_message = str(e)
        logger.exception(f'Exception: {e}')
        return Exception, exception_message

def check_if_elapsed_time_passed(start_time:datetime.datetime, end_time:datetime.datetime, timeout_duration:int) -> bool:
    '''
    Checks if x amount of time passed given a start and endtime with datetime datatype

    Returns:
        bool: Whether the sufficient time has passed
    '''
    time_passed = end_time - start_time
    has_sufficient_time_passed = time_passed >= datetime.timedelta(minutes=timeout_duration)

    return has_sufficient_time_passed