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
def split_and_save_strips(file, pixel_buffer_size=25, max_buffer_count=None, white_threshold=.95, ignore_outer_pct=.2, output_directory=None):
  try:
        filename = file.split("/")[-1].split(".")[0]
        file_ext = file.split("/")[-1].split(".")[-1]
        logging.debug("Processing %s", filename)
        image = Image.open(file)
        image_width = image.size[0]
        image_height = image.size[1]
        logging.debug("Image type: " + image.format + "; mode: " + image.mode + "; dimensions: " + str(image_width) + "x" + str(image_height))
        pixel_map = image.load()

        buffer_indices = []
        buffers_found = 0

        # Go through rows
        # TODO: Add some level of validation to ensure that there's some 100% white rows in the pixel_buffer
        rows = []
        pixels_to_ignore = int(image_height * ignore_outer_pct)
        for y in range(0 + pixels_to_ignore, image_height - pixels_to_ignore):
          avg_white = get_avg_white(image, pixel_map, y)
          if avg_white > white_threshold:
            rows.append(avg_white)
          else:
            if len(rows) >= pixel_buffer_size:
              logging.debug("We've got a winner! Found strip buffer b/t pixels %s and %s", y - len(rows), y)
              buffer_index = y - (len(rows)/2)
              buffer_indices.append(buffer_index)
              buffers_found += 1
            rows.clear()
          logging.debug("%s / %s / %s", y, avg_white, str(avg_white > white_threshold))
        logging.debug("Found %s buffers", buffers_found)
        logging.debug("Buffer indexes to use: %s",str(buffer_indices))
        if len(buffer_indices) == 0:
          if output_directory is None:
            image.show()
          else:
            strip_name = output_directory + filename + '_sunday' + '.' + file_ext
            image.save(strip_name)
        else:
          buffer_indices.append(image_height)
          for i, y in enumerate(buffer_indices):
            prev_pixel = buffer_indices[i-1] if i > 0 else 0
            # (left, upper, right, lower)
            coords = (0, prev_pixel, image_width, y)
            logging.debug("Creating strip from %s", str(coords))
            strip = image.crop(box=coords)
            if output_directory is None:
              strip.show()
            else:
              strip_name = output_directory + filename + '_weekday_' + str(i) + '.' + file_ext
              logging.debug("Saving strip as %s", strip_name)
              strip.save(strip_name)
  except Exception as e:
    logging.error(str(e))
    raise SplitError("Failed to split photo: " + str(e))