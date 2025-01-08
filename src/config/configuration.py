"""This file is designed to manage the configuration parameters"""
from src.constants import *
from src import logger
from src.utils import read_yaml

logger.name = "Configuration Manager"

class ConfigurationManager:
    def __init__(self,
        config_file_path=CONFIG_FILE_PATH,
        params_file_path=PARAMS_FILE_PATH):
        self.config = read_yaml(config_file_path)
        self.params = read_yaml(params_file_path)

    def get_data_ingestion_config(self):
        params = self.params.data_directory
        return params
    
