import logging
import boto3                                # aws client
from pathlib import Path                    # easily identify files


# initialise the logging
logger = logging.getLogger(__name__)

def load_to_s3(data_dir:str, AWS_ACCESS_KEY:str, AWS_SECRET_KEY:str, AWS_BUCKET_NAME:str):
    """Push all json files from a given data directory to S3

    Args:
        data_dir (str): File path of the target directory
        AWS_ACCESS_KEY (str): linked to AWS IAM user
        AWS_SECRET_KEY (str): linked to AWS IAM user
        AWS_BUCKET_NAME (str): S3 bucket to upload to
    """

    # Set up the AWS connection using boto3
    s3_client = boto3.client(
        's3',
        aws_access_key_id = AWS_ACCESS_KEY, 
        aws_secret_access_key = AWS_SECRET_KEY
    )
    logger.info('AWS credentials fetched.')

    # identify all json files to be uploaded 
    json_list = list(Path(data_dir).rglob("*.json"))

    # for loop to iterate through and send to s3
    for file in json_list:
        try:
            s3_client.upload_file(file,AWS_BUCKET_NAME,file.name)
            print(f'File uploaded successfully ({file.name}).')
            logger.info(f'File uploaded successfully ({file.name}) to {AWS_BUCKET_NAME}.')
        except Exception as e:
            print(f'An error has occurred! {e}')
            logger.error(f'An error has occurred! {e}')