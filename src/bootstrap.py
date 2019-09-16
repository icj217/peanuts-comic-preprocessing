from utils.s3 import get_client
from utils.config import get_config
import zipfile
# Updates local environment with S3 data (which we assume to be the latest)
s3 = get_client("s3")
config = get_config()

s3_bucket_name = config["s3"]["bucket_name"]
s3_raw_images = config["s3"]["raw_images"]
s3_cropped_images = config["s3"]["cropped_images"]
local_zip_dir = config["directories"]["zipped_images"]
local_raw_dir = config["directories"]["raw_images"]
local_cropped_dir = config["directories"]["cropped_images"]

# Download Raw Images
local_raw_images_zip = "zippedRawImagesFromS3.zip"
s3.download_file(s3_bucket_name, s3_raw_images, local_zip_dir + local_raw_images_zip)

# Download Raw Images
local_cropped_images_zip = "zippedCroppedImagesFromS3.zip"
s3.download_file(s3_bucket_name, s3_cropped_images, local_zip_dir + local_cropped_images_zip)

# Unzip Files
with zipfile.ZipFile(local_raw_images_zip, 'r') as zip:
  zip.extractall(local_raw_dir)

with zipfile.ZipFile(local_cropped_images_zip, 'r') as zip:
  zip.extractall(local_raw_dir)
