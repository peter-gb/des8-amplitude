import logging
from datetime import datetime   # only need datetime for timestamping filenames
import os                       # for managing files & folders
import requests                 # for making the API calls
import zipfile                  # for unzipping the extracted archive
from pathlib import Path        # for searching through directories
import gzip                     # for opening the gzs
import shutil                   # for saving the gzs as json


# this will generate logs attached to this function, __name__ links the log to this module
logger = logging.getLogger(__name__)


# define the extract function and its inputs
def extract_request(url:str, data_date:str, data_dir:str, AMP_API_KEY:str, AMP_SECRET_KEY:str):
    """Extracts JSON from the specified URL, for yesterday relative to runtime, a data directory is created
           
    Args:
        url (str): give the URL to be visited
        data_date (str): the date for which data is to be fetched
        data_dir (str): Target directory for response payload
        AMP_API_KEY (str): Amplitude API Key
        AMP_SECRET_KEY (str): Amplitude Secret Key
    """
    # Prepare folder and timestamp variables for extracted zip file file name
    os.makedirs(data_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    data_date_dir_name = data_date.strftime("%Y-%m-%d")
    filename = f'{data_dir}/amplitude_{data_date_dir_name}_{timestamp}.zip'

    # define start and end params for request
    start = data_date.strftime("%Y%m%dT00")
    end = data_date.strftime("%Y%m%dT23")

    # log progress
    logger.info(f'Data dir created at {data_dir}. Attempting data fetch for {data_date} at {timestamp}.')

    # Prepare variables for the request
    params = {
        'start': start,
        'end': end
    }

    # GET request with basic auth
    response = requests.get(url, params=params, auth=(AMP_API_KEY, AMP_SECRET_KEY))
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

# # identify the zip and gz files to be deleted
# print("We could delete these gz and zip files")
# logger.info("We could delete these files")
# extensions = {".gz", ".zip"}
# del_files = [f for f in Path(data_dir).rglob("*") if f.suffix in extensions]
# for f in del_files:
#     print(f)
#     logger.info(f)

# # or identify .json to be moved to a json folder instead?
# print("We could move these files")
# logger.info("We could move these json files")
# js_list = Path(data_dir).rglob("*.json")
# for j in js_list:
#     print(j)
#     logger.info(f)