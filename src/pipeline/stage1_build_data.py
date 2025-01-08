#!/usr/bin/env python
from src.features.build_features import FeatureEnginnering
from src.entity.config_entity import FeatureEngineeringConfig
from src.config.configuration import ConfigurationManager
from src.data.make_dataset import DataIngestion
from src.utils.common import (read_pickle, save_pickle, 
                              save_array, save_col_names)
from src import logger
import pandas as pd
import numpy as np

STAGE_NAME = "STAGE 1: BUILD DATA"
logger.name = STAGE_NAME

class FeatureEngineeringTrainPipeline:
    def __init__(self):
        pass

    def main_train(self):
        try:
            data_ingestion = DataIngestion()
            feature_eng = FeatureEnginnering()
            config_manager = ConfigurationManager()
            config_params = config_manager.get_feature_engineering_config()

            # Reading training data
            train = data_ingestion.get_data(config_params.train_dir)
            train = feature_eng.drop_columns(train, config_params.drop_cols)
            x_train, y_train = data_ingestion.split_x_y(train, config_params.target_col)
            
            # save column names 
            save_col_names(x_train, config_params.col_names_to_save)

            # fit encoder-> save encoder -> transform train
            fitter = feature_eng.fit_label_encoder(x_train)
            save_pickle(fitter, config_params.encoder_dir)
            x_train = feature_eng.encoder_transform(fitter, x_train)
            
            # fit standard scalar -> save its object -> transform
            ss_fitter = feature_eng.fit_scalar(x_train)
            save_pickle(ss_fitter, config_params.scalar_dir)
            x_train = feature_eng.scalar_transform(ss_fitter, x_train)
            
            # Saving data
            x_train[config_params.target_col] = y_train
            data_ingestion.save_dataframe(x_train, config_params.processed_train)
        except Exception as e:
            logger.error(e)
            raise e

    def main_test(self):
        try:
            data_ingestion = DataIngestion()
            feature_eng = FeatureEnginnering()
            config_manager = ConfigurationManager()
            config_params = config_manager.get_feature_engineering_config()
            
            # Reading training data
            test = data_ingestion.get_data(config_params.test_dir)
            test = feature_eng.drop_columns(test, config_params.drop_cols)
            x_test, y_train = data_ingestion.split_x_y(test, config_params.target_col)
            
            # Read encoders
            fitter = read_pickle(config_params.encoder_dir)
            ss_fitter = read_pickle(config_params.scalar_dir)

            # transform data
            x_test = feature_eng.encoder_transform(fitter, x_test)
            assert type(x_test) == pd.DataFrame, logger.warning("data not a pandas frame")
            x_test = feature_eng.scalar_transform(ss_fitter, x_test)
            assert type(x_test) == pd.DataFrame, logger.warning("data not a pandas frame")

            # Saving data
            x_test[config_params.target_col] = y_train
            data_ingestion.save_dataframe(x_test, config_params.processed_train)
       
        except Exception as e:
            logger.error(e)
            raise e


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> Train {STAGE_NAME} started <<<<<<")
        obj = FeatureEngineeringTrainPipeline()
        obj.main_train()
        logger.info(f">>>>>> Train {STAGE_NAME} completed <<<<<<\n\nx==========x")
        
        logger.info(f">>>>>> Test {STAGE_NAME} started <<<<<<")
        obj = FeatureEngineeringTrainPipeline()
        obj.main_test()
        logger.info(f">>>>>> Test {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.error(e)
        raise e
