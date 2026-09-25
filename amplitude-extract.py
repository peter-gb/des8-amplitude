# Import packages for the script
import requests                 # for making the API calls
import dotenv                   # for accessing credentials from .env file
import os                       # for managing files & folders
from datetime import datetime   # only need datetime for timestamping filenames

dotenv.load_dotenv()            # load the .env file so credentials are accessible

# Prepare variables for the request

url = 'https://analytics.eu.amplitude.com/api/2/export'

params = {
    'start': '20260924T00',
    'end': '20260924T23'
}

amp_key = os.getenv('AMP_API_KEY')
amp_secret = os.getenv('AMP_SECRET_KEY')

# GET request with basic auth

response = requests.get(url, params=params, auth=(amp_key, amp_secret))

print(response)

