import configparser

def get_config():
  config = configparser.ConfigParser()
  config.read("config/default.ini")
  config.read("config/local.ini")
  return config
