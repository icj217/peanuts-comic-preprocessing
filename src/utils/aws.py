import boto3
from utils.config import get_config

config = get_config()

def get_client(service):
  client = boto3.client(
      service,
      aws_access_key_id=config["aws"]["aws_access_key_id"],
      aws_secret_access_key=config["aws"]["aws_secret_access_key"]
  )
  return client