from PIL import Image, ImageDraw
import pytesseract
import logging
import re

# A strip's publication year and month are available in the bottom corners of the photo
# We don't always know both pieces of information. Only 1 data element is provided per page.
# Need to figure out how to map values from the preceding/following page onto current

def merge_results(a, b):
    logging.debug(str(a))
    logging.debug(str(b))
    c = {}
    for k,v in a.items():
        c[k] = v if v is not None else b[k]
    return c

def parse_tesseract_response(text):
    text = text.upper()
    months = None
    year = None
    page = None
    valid_months = r"(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)"
    valid_year = r"\d{4}"
    valid_page = r"PAGE (\d{1,3})"
    months = re.findall(valid_months, text)
    year = re.search(valid_year, text)
    page = re.search(valid_page, text)
    return {
        'months': months if months != [] else None,
        'year': year.group(0) if year is not None else None,
        'page': page.group(1) if page is not None else None
    }

def get_metadata(file, checkForBanner=True):
    logging.debug("===========================")
    try:
        image = Image.open(file)
        image_width = image.size[0]
        image_height = image.size[1]
        pixel_map = image.load()

        logging.debug("Image type: " + image.format + "; mode: " + image.mode + "; dimensions: " + str(image_width) + "x" + str(image_height))

        border_removed = False
        if checkForBanner == True:
            logging.debug("Checking for banner...")
            banner_color = pixel_map[1, image_height - 1]
            if banner_color == (0,0,0):
                logging.debug("Banner found! Adjusting bottom edge to remove...")
                border_removed = True
                image = image.crop((1, 1, image_width - 1, image_height - 80))
                image_width = image.size[0]
                image_height = image.size[1]
        # Get bottom part of image w/data
        top = image_height - 120 + 40 if border_removed == True else image_height - 120
        bottom = image_height if border_removed == True else image_height - 70
        box = (1, top, image_width - 1, bottom)
        cropped_image = image.crop(box)
        # Split image into left and right images (better chance of tesseract understanding)
        cropped_image_width = cropped_image.size[0]
        cropped_image_height = cropped_image.size[1]
        left_image_box = (0, 0, cropped_image_width/2, cropped_image_height)
        left_image = cropped_image.crop(left_image_box)
        right_image_box = (cropped_image_width/2, 0, cropped_image_width, cropped_image_height)
        right_image = cropped_image.crop(right_image_box)
        # Send to pytesseract
        left_text = pytesseract.image_to_string(left_image)
        right_text = pytesseract.image_to_string(right_image)
        logging.debug("LEFT: %s", left_text)
        logging.debug("RIGHT: %s", right_text)
        # see if we can parse out year/month/page
        left_data = parse_tesseract_response(left_text)
        right_data = parse_tesseract_response(right_text)
        metadata = merge_results(left_data, right_data)
        logging.debug(str(metadata))
        return metadata
    except Exception as e:
        logging.error(e)
        pass