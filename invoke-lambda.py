import multiprocessing 
import time 
import json
import boto3
import botocore
from botocore.config import Config
MAX_RETRIES = 1
BOTO3_CONFIG = Config(connect_timeout=10, read_timeout=10, retries={"max_attempts": MAX_RETRIES})
def get_lambda_client():
    return boto3.client(
        'lambda',
        # aws_access_key_id='',
        # aws_secret_access_key='',
        region_name='us-east-1',
        # endpoint_url=LOCALSTACK_ENDPOINT,
        config=BOTO3_CONFIG
    )  
def invoke_function_and_get_message(function_name,lambda_payload_request):
    start_time = time.time()
    print("Invoking lambda")
    print("\r\nLambda request paylaod")
    print (json.dumps(lambda_payload_request, indent=4, sort_keys=True))
    lambda_client = get_lambda_client()
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        Payload=lambda_payload_request
    )
    end_time = time.time()
    print ("Response in ms -{}".format(end_time-start_time))
    lambda_payload_response = json.loads(
        response['Payload']
        .read()
        .decode('utf-8')
    )
    print("\r\nLambda response paylaod")
    print (json.dumps(lambda_payload_response, indent=4, sort_keys=True))
    return lambda_payload_response

class Process(multiprocessing.Process): 
    def __init__(self, id): 
        super(Process, self).__init__() 
        self.id = id
                 
    def run(self): 
        time.sleep(1) 
        print("I'm the process with id: {}".format(self.id)) 
  
if __name__ == '__main__': 
    p = Process(0) 
    p.start() 
    p.join() 
    p = Process(1) 
    p.start() 
    p.join() 