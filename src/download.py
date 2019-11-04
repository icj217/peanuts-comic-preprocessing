import urllib.request
from utils.config import get_config

files = []

config = get_config()
zip_directory = config["directories"]["zipped_images"]

for file in files:
    filename = file.split('/')[-1]
    print('Downloading', file, 'to', filename)
    localfile = urllib.request.urlretrieve(file, zip_directory + filename)
    print ('Downloaded', filename, '!')
    
