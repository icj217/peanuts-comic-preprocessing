from utils.crop import crop_and_save_image
import logging
from utils.config import get_config

# Logging
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
logging.getLogger().setLevel(logging.DEBUG)

# Config
config = get_config()

file = "{}/tpb-14_100.jpg".format(config["directories"]["raw_images"])

crop_and_save_image(file, padding=20, checkForBanner=True)