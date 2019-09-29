from utils.metadata import get_metadata
import logging
from utils.config import get_config
# Config
config = get_config()

# Logging
format = "%(asctime)s: %(message)s"
logging.basicConfig(filename="{}metadata.log".format(config["directories"]["logs"]),level=logging.INFO)
logging.getLogger().setLevel(logging.DEBUG)


# files = ["tpb-13_268.jpg","tpb-21_276.jpg","tpb-3_64.jpg","tpb-8_151.jpg","tpb-19_220.jpg","tpb-21_328.jpg","tpb-20_329.jpg","tpb-7_12.jpg","tpb-13_247.jpg","tpb-19_218.jpg","tpb-14_172.jpg","tpb-14_100.jpg","tpb-9_241.jpg","tpb-1_16.jpg","tpb-13_17.jpg","tpb-1_29.jpg","tpb-2_152.jpg","tpb-23_262.jpg","tpb-11_16.jpg","tpb-14_18.jpg","tpb-25_11.jpg","tpb-10_328.jpg","tpb-13_238.jpg","tpb-18_13.jpg","tpb-14_124.jpg","tpb-6_330.jpg","tpb-14_142.jpg","tpb-13_328.jpg","tpb-16_331.jpg","tpb-13_262.jpg","tpb-22_75.jpg","tpb-17_18.jpg","tpb-13_277.jpg","tpb-24_15.jpg","tpb-10_15.jpg","tpb-24_328.jpg","tpb-14_178.jpg","tpb-2_317.jpg","tpb-17_332.jpg","tpb-12_328.jpg","tpb-7_325.jpg","tpb-2_328.jpg","tpb-18_98.jpg"]
files = ["tpb-1_262.jpg"] # 
raw_image_directory = config["directories"]["raw_images"]

for file in files:
  try:
    get_metadata("{}/{}".format(raw_image_directory,file))
  except Exception as e:
    logging.info("Failed to get metadata for %s due to error: %s", file, str(e))