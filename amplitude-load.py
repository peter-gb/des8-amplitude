import os                                   # file & folder management
from dotenv import load_dotenv              # credentials access
import boto3                                # aws client
from pathlib import Path                    # easily identify files
from datetime import datetime, timedelta    # datediff and timestamping
from modules.log_initialise import logging_initialise

# initialise the logging
logger = logging_initialise()
logger.info("Logging initialised - let's load!")

# load dotenv credentials
load_dotenv()

aws_access_key = os.getenv('AWS_ACCESS_KEY')
aws_secret_key = os.getenv('AWS_SECRET_KEY')
aws_bucket_name = os.getenv('AWS_BUCKET_NAME')

s3_client = boto3.client(
    's3',
    aws_access_key_id = aws_access_key, 
    aws_secret_access_key = aws_secret_key
)
logger.info('AWS credentials fetched.')

# Prepare folder and timestamp variables for extracted gz files
yesterday = datetime.now() - timedelta(days=1)
yesterday_folder_name = yesterday.strftime("%Y-%m-%d")
data_dir = f'data/zips/{yesterday_folder_name}'


# identify all json files to be uploaded 
json_list = list(Path(data_dir).rglob("*.json"))

# for loop to iterate through and send to s3
for file in json_list:
    try:
        s3_client.upload_file(file,aws_bucket_name,file.name)
        print(f'File uploaded successfully ({file.name}).')
        logger.info(f'File uploaded successfully ({file.name}).')
    except Exception as e:
        print(f'An error has occurred! {e}')
        logger.error(f'An error has occurred! {e}')
