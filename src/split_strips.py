import glob
from utils.config import get_config
from utils.split import split_and_save_strips
import concurrent.futures
import threading
import queue
import time
import logging

config = get_config()
log_directory = config["directories"]["logs"]
source_directory = config["directories"]["cropped_images"]
split_image_directory = config["directories"]["split_images"]

logging.basicConfig(filename="{}split.log".format(log_directory),level=logging.INFO)

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
        files = glob.glob(source_directory + "*")
        for file in files:
            filename = file.split("/")[-1]
            logging.info("Submitting file for splitting: %s", filename)
            pipeline.set_message(file, "producer")
    logging.info("Producer received EXIT event. Exiting")

def splitter(pipeline, event):
    message = 0
    while not event.is_set() or not pipeline.empty():
        message = pipeline.get_message("splitter")
        logging.info("Splitter starting to process file: %s", message)
        try:
            split_and_save_strips(message, output_directory=split_image_directory)
        except Exception as e:
            logging.info("Failed to split %s due to error: %s", message, str(e))

    logging.info("Consumer received EXIT event. Exiting")

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    pipeline = Pipeline()
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(splitter, pipeline, event)
        executor.submit(splitter, pipeline, event)
        executor.submit(splitter, pipeline, event)
        executor.submit(splitter, pipeline, event)
        executor.submit(splitter, pipeline, event)
        executor.submit(splitter, pipeline, event)
        executor.submit(splitter, pipeline, event)
        executor.submit(splitter, pipeline, event)
        time.sleep(0.1)
        logging.info("Main: about to set event")
        event.set()