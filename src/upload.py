import glob
import uuid
import boto3
import logging
from utils.config import get_config

config = get_config()
source_directory = config["directories"]["split_images"]
ddb_table = config["dynamodb"]["table_name"]
s3_bucket = config["s3"]["bucket_name"]

ddb = boto3.client('dynamodb')
s3 = boto3.client('s3')

def put_item(comic_id, book_id, file_name, comic_type):
  item = {
    'comic_id': {
      'S': comic_id
    },
    'book_id': {
      'S': book_id
    },
    'file_name': {
      'S': file_name
    },
    'comic_type': {
      'S': comic_type
    }
  }
  try:
    return ddb.put_item(TableName=ddb_table, Item=item, ConditionalExpression="attribute_not_exists(comic_id)")
  except Exception as e:
    logging.error("Failed to put item %s: %s", comic_id, str(e))

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    try:
        response = s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

files = glob.glob(source_directory)
print('files:', files)
for file in files:
    # Get variables
    file_name = file.split('/')[-1]
    file_parts = file_name[file_name.startswith('tpb-') and len('tpb-'):].split('_')
    book_id = file_parts[0]
    comic_type = file_parts[2]
    # Generate UUID
    comic_id = uuid.uuid4()
    # Insert item into DDB
    put_item(comic_id, book_id, file_name, comic_type)
    # Upload image to S3 under UUID name
    upload_file(comic_id, )