import logging
import os
import yaml


log_dir = "../logs"
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


def read_yaml(path, format="r"):
    try:
        with open(path, "r") as f:
            params = yaml.safe_load(f)
            logging.info("Yaml read successfully from %s", path)
            return params
    except FileNotFoundError:
        logger.error("FileNotFoundError: %s", path)
    except Exception as e:
        logger.error(f"Exception occured while reading yaml file from \
                        location: {path}\n {e}")