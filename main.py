from modules.log_initialise import logging_initialise
from modules.extract_function import extract_request
from dotenv import load_dotenv
import os


# initialise logging
logger = logging_initialise()

# send a logging message to say we are up and running
logger.info("Logger succesfully initialised - let's go!")


# Prepare variables for the request & call the function
url = 'https://analytics.eu.amplitude.com/api/2/export'

# get secrets from dotenv
load_dotenv()
AMP_API_KEY = os.getenv('AMP_API_KEY')
AMP_SECRET_KEY = os.getenv('AMP_SECRET_KEY')

# call the extract function with credentials and URL
extract_request(url, AMP_API_KEY, AMP_SECRET_KEY)

# # prepare secrets for AWS load
# AWS_API_KEY = os.getenv('AWS_API_KEY')
# AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
# AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
