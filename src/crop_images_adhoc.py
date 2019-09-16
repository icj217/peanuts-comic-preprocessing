#!/usr/bin/env python3

from utils.crop import crop_and_save_image
import logging
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
logging.getLogger().setLevel(logging.DEBUG)

file = "/Users/craigburdulis/Repositories/peanuts-comic-preprocessing/downloads/images/raw/tpb-14_100.jpg"

crop_and_save_image(file, padding=20, checkForBanner=True)