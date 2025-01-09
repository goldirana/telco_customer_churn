#!/usr/bin/env python

from src.models.train_model import BuildModel
from src import logger
from src.config.configuration import ConfigurationManager
from src.data.make_dataset import DataIngestion
import dagshub


STAGE_NAME =  "STAGE 2: BUILD MODEL"
logger.name = STAGE_NAME

class BuildModelPipeline:
    def __init__(self):
        pass

    def main(self):
        config_manager = ConfigurationManager()
        config_params = config_manager.get_model_building_config()
        dags_params = config_manager.get_dagshub_config()
    
        build_model = BuildModel(config_params,
                                 dags_params)
        data_ingestion = DataIngestion()
        train = data_ingestion.get_data(config_params.train_dir)
        x_train, y_train = data_ingestion.split_x_y(train, config_params.target_col)
        build_model.fit(x_train, y_train)



if __name__ == "__main__":
    try:
        logger.info(f">>>>>> Train {STAGE_NAME} started <<<<<<")
        obj = BuildModelPipeline()
        obj.main()
        logger.info(f">>>>>> Train {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.error(e)
        raise e