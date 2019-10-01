import glob
import uuid
import boto3
import logging
import csv
import sys
import re
import arrow
import random
from utils.aws import get_client
from time import strptime
from utils.config import get_config

config = get_config()
log_directory = config["directories"]["logs"]
source_directory = 'files/images/split_full/*' # config["directories"]["split_images"]
ddb_table = config["dynamodb"]["table_name"]
s3_bucket = config["s3"]["public_bucket_name"]

ddb = get_client('dynamodb')
s3 = get_client('s3')

logging.basicConfig(filename="{}upload.log".format(log_directory),level=logging.INFO)

def put_item(item):
  try:
    return ddb.put_item(TableName=ddb_table, Item=item, ConditionExpression="attribute_not_exists(comic_id) AND attribute_not_exists(display_date)")
  except Exception as e:
    logging.error("Failed to put item %s: %s", comic_id, str(e))

def upload_file(file_name, bucket, object_name=None, ExtraArgs={}):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name
    # Upload the file
    try:
        s3.upload_file(file_name, bucket, object_name, ExtraArgs)
    except Exception as e:
        logging.error(e)
        return False
    return True

report_file_name = sys.argv[1]

with open(report_file_name, newline='') as report:
  # Load metadata into dict
  reader = csv.DictReader(report, delimiter=',', quotechar='"')
  metadata = { rows['file'].split('/')[-1]:rows for rows in reader }
  # Define start date
  time = arrow.utcnow()
  # Iterate through files
  files = glob.glob(source_directory)
  random.shuffle(files)
  file_count = len(files)
  processed_count = 0
  error_count = 0
  for file in files:
    # Get variables
    file_name = file.split('/')[-1]
    file_ext = file.split('.')[-1]
    file_parts = file_name.split('_')
    original_file_name = file_parts[0] + '_' + file_parts[1] + '.' + file_ext
    book_id = file_parts[0].replace('tpb-', '')
    comic_type = file_parts[2]
    page_metadata = metadata.get(original_file_name)
    book_num = page_metadata['book']
    page_num = page_metadata['page2']
    pub_year = page_metadata['year']
    pub_months = re.findall(r"'(.*?)'", str(page_metadata['months'])) or []
    pub_month = str(strptime(pub_months[0],'%B').tm_mon)
    display_date = time.date().isoformat()
    is_bt_months = len(pub_months) > 1
    # Generate UUID
    comic_id = str(uuid.uuid4())
    # Generate URL (should we use bucket name or something more stable?)
    url = 'https://{}.s3.amazonaws.com/strips/{}'.format(s3_bucket, comic_id)
    # Build Item
    item = {}
    item['comic_id'] = { 'S': comic_id }
    item['url'] = { 'S': url }
    item['comic_type'] = { 'S': comic_type }
    item['book_num'] = { 'N': book_num }
    item['page_num'] = { 'N': page_num }
    item['pub_year'] = { 'N': pub_year }
    item['pub_month'] = { 'N': pub_month }
    item['pub_day'] = { 'N': '0' }
    item['display_date'] = { 'S': display_date }
    item['original_file_name'] = { 'S': file_name }
    item['is_bt_months'] = { 'BOOL': is_bt_months }
    if len(pub_months) > 1:
      item['bt_months'] = { 'SS': pub_months }
    try:
      # Insert item into DDB
      put_item(item)
      # Upload image to S3 under UUID name
      upload_file(file, s3_bucket, 'strips/' + comic_id, ExtraArgs={'ContentType': 'image/jpeg', 'ACL': 'public-read'})
      # Increment day
      time = time.shift(days=1)
      processed_count += 1
      print("processed: {}/{}".format(processed_count, file_count))
    except Exception as e:
      error_count += 1
      logging.error("Failed to upload/insert file: %s", str(e))
  logging.info("Finished with %s success and %s errors", str(processed_count), str(error_count))