"""This file is designed to manage the configuration parameters"""
from src.constants import *
from src import logger
from src.utils.common import read_yaml
from src.entity.config_entity import DataIngestionConfig

logger.name = "Configuration Manager"

class ConfigurationManager:
    def __init__(self,
        config_file_path=CONFIG_FILE_PATH,
        params_file_path=PARAMS_FILE_PATH):
        self.config = read_yaml(config_file_path)
        self.params = read_yaml(params_file_path)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        data_ingestion_config = DataIngestionConfig(
            root_dir=self.config.data_directory.root_dir,
            train_dir=self.config.data_directory.interim_train,
            test_dir=self.config.data_directory.interim_test,
            test_size=self.params.make_dataset.test_size)
        return data_ingestion_config
