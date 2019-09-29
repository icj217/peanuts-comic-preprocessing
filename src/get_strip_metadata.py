import glob
from utils.metadata import get_metadata
from utils.config import get_config
import concurrent.futures
import threading
import queue
import time
import logging
import csv

config = get_config()
log_directory = config["directories"]["logs"]
raw_image_directory = config["directories"]["raw_images"]

logging.basicConfig(filename="{}metadata.log".format(log_directory),level=logging.INFO)

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
            logging.info("Submitting file for metadata: %s", filename)
            pipeline.set_message(file, "producer")
    logging.info("Producer received EXIT event. Exiting")

def metadata(pipeline, event):
    message = 0
    while not event.is_set() or not pipeline.empty():
        message = pipeline.get_message("metadata")
        logging.debug("Metadata getter starting to process file: %s", message)
        try:
            metadata = get_metadata(message)
            logging.info("SUCCESS\t%s\t%s\t%s\t%s", message, metadata['months'], metadata['year'], metadata['page'])
        except Exception as e:
            logging.info("Failed to get metadata for %s due to error: %s", message, str(e))

    logging.info("Consumer received EXIT event. Exiting")

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    pipeline = Pipeline()
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(metadata, pipeline, event)
        executor.submit(metadata, pipeline, event)
        executor.submit(metadata, pipeline, event)
        executor.submit(metadata, pipeline, event)
        executor.submit(metadata, pipeline, event)
        executor.submit(metadata, pipeline, event)
        executor.submit(metadata, pipeline, event)
        executor.submit(metadata, pipeline, event)
        time.sleep(0.1)
        logging.info("Main: about to set event")
        event.set()