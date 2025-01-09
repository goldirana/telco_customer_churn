import logging
import os
import yaml
from pathlib import Path

log_dir = "logs"
log_dir = str(Path(log_dir).resolve())
log_file_name = "running.log"
# create logs dir
os.makedirs(log_dir, exist_ok=True)
# basic logging configuration

file_handler = logging.FileHandler(filename=os.path.join(log_dir,
                                                         log_file_name))
stream_handler = logging.StreamHandler()
logging_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logging.basicConfig(
    level=logging.DEBUG,
    format=logging_format,
    handlers=[file_handler, stream_handler]
)
logger = logging.getLogger("Initializing logging")


