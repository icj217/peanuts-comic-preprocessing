import glob
import uuid
import boto3
import logging
import csv
import sys
import re
import arrow
from utils.config import get_config

config = get_config()
source_directory = config["directories"]["split_images"]
ddb_table = config["dynamodb"]["table_name"]
s3_bucket = config["s3"]["bucket_name"]

ddb = boto3.client('dynamodb')
s3 = boto3.client('s3')

def put_item(item):
  try:
    return ddb.put_item(TableName=ddb_table, Item=item, ConditionalExpression="attribute_not_exists(comic_id) AND attribute_not_exists(display_date)")
  except Exception as e:
    logging.error("Failed to put item %s: %s", comic_id, str(e))

def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    try:
        s3.upload_file(file_name, bucket, object_name)
    except Exception as e:
        logging.error(e)
        return False
    return True

report_file_name = sys.argv[1]

with open(report_file_name, newline='') as report:
  # Load metadata into dict
  reader = csv.DictReader(report, delimiter=',', quotechar='"')
  metadata = { rows[0].split('/')[-1]:rows for rows in reader }
  # Define start date
  time = arrow.utcnow()
  # Iterate through files
  files = glob.glob(source_directory)
  for file in files:
    # Get variables
    file_name = file.split('/')[-1]
    file_ext = file.split('.')[-1]
    file_parts = file_name.split('_')
    original_file_name = file_parts[0] + '.' + file_ext
    book_id = file_parts[0].replace('tpb-', '')
    comic_type = file_parts[2]
    page_metadata = metadata.get(file_name)
    book_num = page_metadata['book']
    page_num = page_metadata['page2']
    pub_year = page_metadata['year']
    pub_month = re.findall(r"'(.*?)'", str(page_metadata['months'])) or []
    display_date = time.date().isoformat()
    is_bt_months = len(pub_month) > 1
    # Generate UUID
    comic_id = uuid.uuid4()
    # Generate URL (should we use bucket name or something more stable?)
    url = 'https://{}.s3.amazonaws.com/strips/{}'.format(s3_bucket, comic_id)
    # Build Item
    item = {}
    item['comic_id'] = { 'S': comic_id }
    item['url'] = { 'S': url }
    item['comic_type'] = { 'S': comic_type }
    item['book_num'] = { 'N': page_metadata }
    item['page_num'] = { 'N': page_metadata }
    item['pub_year'] = { 'N': page_metadata }
    item['pub_month'] = { 'N': page_metadata }
    item['pub_day'] = { 'NULL': True }
    item['display_date'] = { 'S': display_date }
    item['original_file_name'] = { 'S': file_name }
    item['is_bt_months'] = { 'BOOL': is_bt_months }
    try:
      # Insert item into DDB
      put_item(item)
      # Upload image to S3 under UUID name
      upload_file(file, s3_bucket, comic_id)
      # Increment day
      time.shift(days=1)
    except Exception as e:
      logging.error("Failed to upload/insert file: %s", str(e))