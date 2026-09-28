import os                               # file & folder management
from dotenv import load_dotenv          # credentials access
import boto3                            # aws client

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


test_upload = 'data/zips/2026-09-27/100011471/100011471_2026-09-27_0#0.json'
filename = '100011471_2026-09-27_0#0.json'

print(f"Uploading file: {test_upload}")
print(f"Bucket name: {aws_bucket_name}")
print(f"S3 Key: {filename}")

s3_client.upload_file(test_upload,aws_bucket_name,filename)