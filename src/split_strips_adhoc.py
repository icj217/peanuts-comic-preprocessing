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
dest_directory = config["directories"]["split_images"]


# Early image (bigger spacing)
# file = "{}/tpb-1_13.jpg".format(config["directories"]["cropped_images"])

# Later image (less spacing)
# file = "{}/tpb-12_43.jpg".format(config["directories"]["cropped_images"])

# Sunday comic
file = "{}/tpb-6_167.jpg".format(config["directories"]["cropped_images"])

# Problem with splitting
file = "{}/tpb-20_111.jpg".format(config["directories"]["cropped_images"])



split_and_save_strips(file, white_threshold=.992, pixel_buffer=20)