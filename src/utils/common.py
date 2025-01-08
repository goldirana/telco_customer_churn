import json, yaml
from src import logger

def read_yaml(path, format="r"):
    try:
        with open(path, "r") as f:
            params = yaml.safe_load(f)
            logger.info("Yaml read successfully from %s", path)
            return params
    except FileNotFoundError:
        logger.error("FileNotFoundError: %s", path)
    except Exception as e:
        logger.error(f"Exception occured while reading yaml file from \
                        location: {path}\n {e}")