from utils.split import split_and_save_strips
import logging
from utils.config import get_config

# Logging
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
logging.getLogger().setLevel(logging.DEBUG)

# Config
config = get_config()

# Early image (bigger spacing)
# file = "{}/tpb-1_13.jpg".format(config["directories"]["cropped_images"])
file = "{}/tpb-9_325.jpg".format(config["directories"]["cropped_images"])


split_and_save_strips(file, white_threshold=.95)