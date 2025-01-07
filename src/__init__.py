import logging
import os

log_dir = "logs"
log_file_name = "running.log"
# create logs dir
os.makedirs(os.join.path(log_dir, log_file_name), exist_ok=True)
# basic logging configuration

file_handler = logging.FileHandler(filename=os.path.join(log_dir,
                                                         log_file_name))
stream_handler = logging.StreamHandler()
logging_format = "%(asctime)s - %(name)s - %(level)s - %(msg)s"

logging.basicConfig(
    level=logging.DEBUG,
    format=logging_format,
    handlers=[file_handler, stream_handler]
)
logger = logging.getLogger("Initializing logging")