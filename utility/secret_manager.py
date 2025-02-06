import boto3
from botocore.exceptions import ClientError
import json
from datetime import datetime,timedelta

secrets_cache = None
secrets_cache_exp = None

secret_duration_mins = 1440

def store_cache(secret):
    global secrets_cache
    global secrets_cache_exp

    secrets_cache = secret
    secrets_cache_exp = datetime.now() + timedelta(minutes=secret_duration_mins)

def cache_checker():
    if secrets_cache_exp:
        exp = True if secrets_cache_exp <= datetime.now() else False
    return True

def get_secret(secret_key:str,secret_name:str):
    '''
    Connects to aws secret manager
        Returns:
            String
    '''

    is_expired = cache_checker()
    print(f'{secrets_cache_exp=}')
    print(f'{secrets_cache_exp=}')
    print(f'{is_expired=}')

    if secrets_cache and not is_expired:
        return secrets_cache.get(secret_key) 

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
    print(f'{secret_dict=}')
    store_cache(secret_dict)


    return secret_dict.get(secret_key)