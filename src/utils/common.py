import json, yaml
from src import logger
from box import ConfigBox
from ensure import ensure_annotations
import os
from pathlib import Path
from typing import Any
import pickle


def create_directory(path: str, is_extension_present: bool=True)-> None:
    """Create directory at given location
    
    Args:
        path(str): path where directory needs to be created
        is_extension_present: whether extension of file present in path
            If present then extract the root path and creates directory"""
    if is_extension_present: # remove extension to create directory
            path = str(split_file_extension(path))
    _ = check_directory_path(path)
    try:
        if _ == False:
            os.makedirs(path, exist_ok=True) # create directoy at given location
            logger.info("Creating directory at %s", path)
        else: 
            os.makedirs(str(path), exist_ok=True)
            logger.info("Deleting previous directory and creating directory at %s", path)
    except Exception as e:
        logger.error(f"Error occured while creating directory at {path} \n{e}")

def split_file_extension(path: str) -> str:
    """
    To remove the extension name from the given path
    Args:
        path: str
    """
    try:
        root_dir = str(Path(path).resolve().parent)
        logger.debug("File path without extension is %s", root_dir)
        return root_dir
    except Exception as e:
        logger.error(e)


def check_directory_path(path: str) -> None:
    """
    To check whether directory presents at given location
    Args:
        path(str)
    Return:
        Boolean
    """
    try:
        check = os.path.isdir(path)
        if check:
            logger.info("Directory already present at %s", path)
            return True
        else:
            logger.info("Directory not present at %s", path)
            return False
    except Exception as e:
        logger.error(e)

@ensure_annotations
def read_yaml(path: str, format: str="r"):
    try:
        with open(path, "r") as f:
            params = yaml.safe_load(f)
            logger.info("Yaml read successfully from %s", path)
            return ConfigBox(params)
    except FileNotFoundError:
        logger.error("FileNotFoundError: %s", path)
    except Exception as e:
        logger.error(f"Exception occured while reading yaml file from \
                        location: {path}\n {e}")
        
def save_pickle(object: Any, path: str):
    try:
        create_directory(path, is_extension_present=True)
        with open(path, "wb") as f:
            pickle.dump(object, f)
        logger.info("Pickle object stored at %s", path)
    except pickle.PickleError as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)

def read_pickle(path: str):
    try:
        path = str(Path(path).resolve())
        print(path)
        with open(path, "rb") as f:
            params = pickle.load(f)
            return params
    except Exception as e:
        logger.error("Error occured while reading pickle %s", e)