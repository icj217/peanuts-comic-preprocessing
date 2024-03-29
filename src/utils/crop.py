#pylint: disable-msg=too-many-format-args
from PIL import Image, ImageDraw
from statistics import mean
import logging

class CropError(Exception):
    pass

def crop_and_save_image(file, output_directory=None, padding=0, only_near_borders=True, checkForBanner=False):
    try:
        filename = file.split("/")[-1]
        image = Image.open(file)
        image_width = image.size[0]
        image_height = image.size[1]

        logging.debug("Image type: " + image.format + "; mode: " + image.mode + "; dimensions: " + str(image_width) + "x" + str(image_height))

        pixel_map = image.load()

        border_offset = 1
        if checkForBanner == True:
            logging.debug("Checking for banner...")
            banner_color = pixel_map[1, image_height - 1]
            if banner_color == (0,0,0):
                logging.debug("Banner found! Adjusting bottom edge to remove...")
                border_offset = 80

        # Walk across each row from top to bottom, stop when we get to row where majority is black
        topBorder = None
        for y in range(0, image_height - border_offset):
            row = []
            for x in range(0, image_width - 1):
                pixel = pixel_map[x,y]
                percentWhite = ((pixel[0] + pixel[1] + pixel[2]) / 3) / 255
                row.append(percentWhite)
            avgAmountOfWhite = mean(row)
            logging.debug("TOP | %s | %s white", y, avgAmountOfWhite)
            if only_near_borders and avgAmountOfWhite < .8:
                logging.debug("Found top row with %s at pixel %s", avgAmountOfWhite, y)
                if y > (.25 * image_height):
                    raise CropError("Top pixel {} is beyond limit".format(y))
                topBorder = y
                break

        bottomBorder = None
        for y in range(image_height - border_offset, 0, -1):
            row = []
            for x in range(0, image_width - 1):
                pixel = pixel_map[x,y]
                percentWhite = ((pixel[0] + pixel[1] + pixel[2]) / 3) / 255
                row.append(percentWhite)
            avgAmountOfWhite = mean(row)
            logging.debug("BOTTOM | %s | %s white", y, avgAmountOfWhite)
            if avgAmountOfWhite < .8:
                logging.debug("Found bottom row with %s white at pixel %s", avgAmountOfWhite, y)
                if only_near_borders and y < (.75 * image_height):
                    raise CropError("Bottom pixel {} is beyond limit".format(y))
                bottomBorder = y
                break

        leftBorder = None
        for x in range(0, image_width - 1):
            row = []
            for y in range(0, image_height - border_offset):
                pixel = pixel_map[x,y]
                percentWhite = ((pixel[0] + pixel[1] + pixel[2]) / 3) / 255
                row.append(percentWhite)
            avgAmountOfWhite = mean(row)
            logging.debug("LEFT | %s | %s white", x, avgAmountOfWhite)
            if avgAmountOfWhite < .9:
                logging.debug("Found left column with %s white at pixel %s", avgAmountOfWhite, x)
                if only_near_borders and x > (.25 * image_width):
                    raise CropError("Left pixel {} is beyond limit".format(x))
                leftBorder = x
                break
        rightBorder = None
        for x in range(image_width - 1, 0, -1):
            row = []
            for y in range(0, image_height - border_offset):
                pixel = pixel_map[x,y]
                percentWhite = ((pixel[0] + pixel[1] + pixel[2]) / 3) / 255
                row.append(percentWhite)
            avgAmountOfWhite = mean(row)
            logging.debug("RIGHT | %s | %s white", x, avgAmountOfWhite)
            if avgAmountOfWhite < .8:
                logging.debug("Found right column with %s white at pixel %s", avgAmountOfWhite, x)
                if only_near_borders and x < (.75 * image_width):
                    raise CropError("Right pixel {} is beyond limit".format(x))
                rightBorder = x
                break
        logging.debug("Borders: %s top / %s bottom / %s left / %s right", topBorder, bottomBorder, leftBorder, rightBorder)

        if not topBorder or not bottomBorder or not leftBorder or not rightBorder:
            error_message = "Did not find one of the coordinates: {} top / {} bottom / {} left / {} right".format(topBorder, bottomBorder, leftBorder, rightBorder)
            raise CropError(error_message)
        cropped_image = image.crop((leftBorder - padding, topBorder - padding, rightBorder + padding, bottomBorder + padding))
        if output_directory:
            cropped_image.save(output_directory + filename)
        else:
            cropped_image.show()
    except Exception as e:
        logging.error(str(e))
        raise CropError("Failed to crop photo: " + str(e))