# Import packages for the script
import requests                 # for making the API calls
import dotenv                   # for accessing credentials from .env file
import os                       # for managing files & folders
from datetime import datetime   # only need datetime for timestamping filenames
import zipfile                  # for unzipping the extracted archive
import gzip                     # for unzipping the gzs to json
# import json                     # for processing json
import shutil
from pathlib import Path

# Prepare folder and timestamp variables for extracted zip file file name
data_dir = 'data/zips'
os.makedirs(data_dir, exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f'{data_dir}/amplitude_{timestamp}.zip'


# Prepare variables for the request
url = 'https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': '20260924T00',
    'end': '20260924T23'
}

# Retrieve and prepare API Credentials
dotenv.load_dotenv()                        # load the .env file so credentials are accessible
amp_key = os.getenv('AMP_API_KEY')
amp_secret = os.getenv('AMP_SECRET_KEY')

# GET request with basic auth
response = requests.get(url, params=params, auth=(amp_key, amp_secret))
status = response.status_code
print(status)

# Write the response as a .zip file
with open(filename, "wb") as file:          # wb here means write binary as we don't have text but a zip
    file.write(response.content)

gz_list = []

# use zipfile to extract the contents of the zip
with zipfile.ZipFile(filename) as zip_ref:
    zip_ref.extractall(path = data_dir)
    print("Extracted files:")
    for ext_file in zip_ref.namelist():
        print(ext_file)



####### ALL NEEDS DOCUMENTING ###################################

# identify the gz files to be extracted to json
gz_list = Path(data_dir).rglob("*.json.gz")

# extract to json files
for gz in map(Path,gz_list):
    dest = gz.with_suffix("")
    with gzip.open(gz,"rb") as f_in, open(dest, "wb") as f_out:
        shutil.copyfileobj(f_in,f_out)
    print(f"{gz} -> {dest}")



# identify the zip and gz files to be deleted
print("We could delete these files")
extensions = {".gz", ".zip"}
del_files = [f for f in Path(data_dir).rglob("*") if f.suffix in extensions]
for f in del_files:
    print(f)

# or identify .json to be moved to a json folder instead?
print("We could move these files")
js_list = Path(data_dir).rglob("*.json")
for j in js_list:
    print(j)
