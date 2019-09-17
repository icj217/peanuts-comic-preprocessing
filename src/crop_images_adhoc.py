from utils.crop import crop_and_save_image
import logging
from utils.config import get_config
# Config
config = get_config()

# Logging
format = "%(asctime)s: %(message)s"
logging.basicConfig(filename="{}crop.log".format(config["directories"]["logs"]),level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)


files = ["tpb-13_268.jpg","tpb-21_276.jpg","tpb-3_64.jpg","tpb-8_151.jpg","tpb-19_220.jpg","tpb-21_328.jpg","tpb-20_329.jpg","tpb-7_12.jpg","tpb-13_247.jpg","tpb-19_218.jpg","tpb-14_172.jpg","tpb-14_100.jpg","tpb-9_241.jpg","tpb-1_16.jpg","tpb-13_17.jpg","tpb-1_29.jpg","tpb-2_152.jpg","tpb-23_262.jpg","tpb-11_16.jpg","tpb-14_18.jpg","tpb-25_11.jpg","tpb-10_328.jpg","tpb-13_238.jpg","tpb-18_13.jpg","tpb-14_124.jpg","tpb-6_330.jpg","tpb-14_142.jpg","tpb-13_328.jpg","tpb-16_331.jpg","tpb-13_262.jpg","tpb-22_75.jpg","tpb-17_18.jpg","tpb-13_277.jpg","tpb-24_15.jpg","tpb-10_15.jpg","tpb-24_328.jpg","tpb-14_178.jpg","tpb-2_317.jpg","tpb-17_332.jpg","tpb-12_328.jpg","tpb-7_325.jpg","tpb-2_328.jpg","tpb-18_98.jpg"]
cropped_image_directory = config["directories"]["cropped_images"]
raw_image_directory = config["directories"]["raw_images"]
for file in files:
  try:
    crop_and_save_image("{}/{}".format(raw_image_directory,file), output_directory=cropped_image_directory, padding=20, checkForBanner=True)
  except Exception as e:
    logging.info("Failed to crop %s due to error: %s", file, str(e))