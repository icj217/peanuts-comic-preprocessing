import glob
import zipfile
from utils.config import get_config

config = get_config()
zip_directory = '{}*'.format(config["directories"]["zipped_images"])
image_directory = config["directories"]["raw_images"]

files = glob.glob(zip_directory)
print('files:', files)
for file in files:
    filename = file.split('/')[-1]
    print('Unzipping contents of', filename)
    with zipfile.ZipFile(file, 'r') as zip:
        for zip_info in zip.infolist():
            if zip_info.filename[-1] == '/':
                continue
            zip_info.filename = filename.replace('.zip', '') + '_' + zip_info.filename
            zip.extract(zip_info, image_directory)