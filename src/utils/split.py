#pylint: disable-msg=too-many-format-args
from PIL import Image, ImageDraw
from statistics import mean
import logging

class SplitError(Exception):
    pass

def get_avg_white(image, pixels, row):
  levels = []
  for x in range(0, image.size[0] - 1):
      pixel = pixels[x,row]
      percentWhite = ((pixel[0] + pixel[1] + pixel[2]) / 3) / 255
      levels.append(percentWhite)
  return mean(levels)

"""
Walk the image vertically, going row by row and calculating/saving % white
When we reach X number of consecutive rows above threshold of white (e.g. 90%), we know we're between strips
X must be greater than the spacing between boxes in the Sunday comics

"""
def split_and_save_strips(file, pixel_buffer=25, white_threshold=.9, ignore_outer_pct=.2, output_directory=None):
  try:
        filename = file.split("/")[-1]
        logging.debug("Processing %s", filename)
        image = Image.open(file)
        image_width = image.size[0]
        image_height = image.size[1]
        logging.debug("Image type: " + image.format + "; mode: " + image.mode + "; dimensions: " + str(image_width) + "x" + str(image_height))
        pixel_map = image.load()

        # Go through rows
        rows = []
        buffers_found = 0
        pixels_to_ignore = int(image_height * ignore_outer_pct)
        for y in range(0 + pixels_to_ignore, image_height - pixels_to_ignore):
          avg_white = get_avg_white(image, pixel_map, y)
          if avg_white > white_threshold:
            rows.append(avg_white)
          else:
            if len(rows) >= pixel_buffer:
              logging.debug("We've got a winner! Found strip buffer b/t pixels %s and %s", y - len(rows), y)
              buffers_found += 1
            rows.clear()
          logging.debug("%s / %s / %s", y, avg_white, str(avg_white > white_threshold))
        logging.debug("Found %s buffers", buffers_found)
  except Exception as e:
    logging.error(str(e))
    raise SplitError("Failed to split photo: " + str(e))