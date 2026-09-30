from modules.log_initialise import logging_initialise
from modules.extract_function import extract_request
from dotenv import load_dotenv
import os
from modules.load_function import load_to_s3
from datetime import datetime, timedelta

# initialise logging
logger = logging_initialise()

# send a logging message to say we are up and running
logger.info("Logger succesfully initialised - let's go!")


# Prepare variables for the request & call the function
url = 'https://analytics.eu.amplitude.com/api/2/export'

# prepare the data directory using yesterday's date
data_date = datetime.now() - timedelta(days=1)
data_date_dir_name = data_date.strftime("%Y-%m-%d")
data_dir = f'data/zips/{data_date_dir_name}'


# get secrets from dotenv
load_dotenv()

# amplitude
AMP_API_KEY = os.getenv('AMP_API_KEY')
AMP_SECRET_KEY = os.getenv('AMP_SECRET_KEY')

# aws s3
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')


# call the extract function with credentials and URL
extract_request(url, data_date, data_dir, AMP_API_KEY, AMP_SECRET_KEY)

# call the load function with credentials inc bucket name
load_to_s3(data_dir,AWS_ACCESS_KEY,AWS_SECRET_KEY,AWS_BUCKET_NAME)
