import requests                 # for making the API calls
import dotenv                   # for accessing credentials from .env file
import os                       # for managing files & folders
from datetime import datetime   # only need datetime for timestamping filenames
from datetime import timedelta  # for datediff
import zipfile                  # for unzipping the extracted archive
import gzip                     # for unzipping the gzs to json
import shutil
from pathlib import Path
from modules.log_initialise import logging_initialise

# initialise logging
logger = logging_initialise()

# send a logging message to say we are up and running
logger.info("Logger succesfully initialised - let's go!")


# Prepare folder and timestamp variables for extracted zip file file name
yesterday = datetime.now() - timedelta(days=1)
yesterday_folder_name = yesterday.strftime("%Y-%m-%d")
data_dir = f'data/zips/{yesterday_folder_name}'
os.makedirs(data_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f'{data_dir}/amplitude_{yesterday_folder_name}_{timestamp}.zip'

start = yesterday.strftime("%Y%m%dT00") 
end = yesterday.strftime("%Y%m%dT23") 

# log progress
logger.info(f'Data dir created at {data_dir}. Attempting data fetch for {yesterday_folder_name} at {timestamp}.')


# Prepare variables for the request
url = 'https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': start,
    'end': end
}

# Retrieve and prepare API Credentials
dotenv.load_dotenv()                        # load the .env file so credentials are accessible
amp_key = os.getenv('AMP_API_KEY')
amp_secret = os.getenv('AMP_SECRET_KEY')

# GET request with basic auth
response = requests.get(url, params=params, auth=(amp_key, amp_secret))
status = response.status_code
print(status)
logger.info(f'API request made. Repsonse status code: {status}')

# Write the response as a .zip file
with open(filename, "wb") as file:          # wb here means write binary as we don't have text but a zip
    file.write(response.content)
    logger.info(f'Wrote {filename}')


# use zipfile to extract the contents of the zip
with zipfile.ZipFile(filename) as zip_ref:
    zip_ref.extractall(path = data_dir)
    print("Extracted files:")
    for ext_file in zip_ref.namelist():
        print(ext_file)
        logger.info(f'Extracted {ext_file}')


# identify the gz files to be extracted to json
gz_list = Path(data_dir).rglob("*.json.gz")

# extract to json files
for gz in map(Path,gz_list):
    dest = gz.with_suffix("")
    with gzip.open(gz,"rb") as f_in, open(dest, "wb") as f_out:
        shutil.copyfileobj(f_in,f_out)
    print(f'{gz} -> {dest}')
    logger.info(f'{gz} converted to {dest}')

##### Process done here #### Nice to have is the following file management:

# identify the zip and gz files to be deleted
print("We could delete these gz and zip files")
logger.info("We could delete these files")
extensions = {".gz", ".zip"}
del_files = [f for f in Path(data_dir).rglob("*") if f.suffix in extensions]
for f in del_files:
    print(f)
    logger.info(f)

# or identify .json to be moved to a json folder instead?
print("We could move these files")
logger.info("We could move these json files")
js_list = Path(data_dir).rglob("*.json")
for j in js_list:
    print(j)
    logger.info(f)