import glob
from utils.crop import crop_and_save_image
from utils.config import get_config
import concurrent.futures
import threading
import queue
import time
import logging

config = get_config()
log_directory = config["directories"]["logs"]
raw_image_directory = config["directories"]["raw_images"]
cropped_image_directory = config["directories"]["cropped_images"]

logging.basicConfig(filename="{}crop.log".format(log_directory),level=logging.INFO)

SENTINEL = object()

class Pipeline(queue.Queue):
    def __init__(self):
        super().__init__(maxsize=10)

    def get_message(self, name):
        value = self.get()
        return value

    def set_message(self, value, name):
        self.put(value)

def producer(pipeline, event):
    while not event.is_set():
        files = glob.glob(raw_image_directory + "*")
        for file in files:
            filename = file.split("/")[-1]
            logging.info("Submitting file for cropping: %s", filename)
            pipeline.set_message(file, "producer")
    logging.info("Producer received EXIT event. Exiting")

def cropper(pipeline, event):
    message = 0
    while not event.is_set() or not pipeline.empty():
        message = pipeline.get_message("cropper")
        logging.info("Cropper starting to process file: %s", message)
        try:
            crop_and_save_image(message, output_directory=cropped_image_directory, padding=20, checkForBanner=True)
        except Exception as e:
            logging.info("Failed to crop %s due to error: %s", message, str(e))

    logging.info("Consumer received EXIT event. Exiting")

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    pipeline = Pipeline()
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(cropper, pipeline, event)
        executor.submit(cropper, pipeline, event)
        executor.submit(cropper, pipeline, event)
        executor.submit(cropper, pipeline, event)
        executor.submit(cropper, pipeline, event)
        executor.submit(cropper, pipeline, event)
        executor.submit(cropper, pipeline, event)
        executor.submit(cropper, pipeline, event)
        time.sleep(0.1)
        logging.info("Main: about to set event")
        event.set()