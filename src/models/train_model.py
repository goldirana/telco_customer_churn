#!/usr/bin/env python
from src.utils.common import read_pickle, read_yaml, read_array
from src.data.make_dataset import DataIngestion
from src.constants import *
from src import logger
from dataclasses import dataclass
from box import ConfigBox
from typing import Optional
from src.config.configuration import ModelBuildingConfig

# model building
import sklearn as sk
from importlib import import_module
import mlflow


STAGE_NAME = "STAGE 2: MODEL BUILDING"
logger.name = STAGE_NAME

class BuildModel:
    def __init__(self, config: ModelBuildingConfig):
        self.config = config

    def get_model_class(self):
        try:
            module = import_module(f"sklearn.{self.config.sub_module}")
            model_class = getattr(module, self.config.model_name)
            logger.info(f"{self.config.model_name} sucessfully returned")
            return model_class
        except ModuleNotFoundError as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)

    def log_metrics(self, model, metrics: list, y_true, y_pred, data_name:str="Train"):
        try:
            for metric in metrics:
                module = import_module("sklearn.metrics")
                metric_func = getattr(module, metric)
                mlflow.log_metric(data_name +" "+ metric_func.__name__, metric_func(y_true, y_pred))
            logger.info("Metrics logged sucessfully")
        except Exception as e:
            logger.error(e)
            raise e

    def fit(self, x_train, y_train):
        try:
            model = self.get_model_class()
            # initiating model
            mlflow.set_experiment(self.config.experiment_name)
            mlflow.start_run()
            model = model()
            # fit model
            model.fit(x_train, y_train)
            logger.info("Model Fitted sucessfully")
            self.save_model(model, self.config.save_model_path)
            y_pred = model.predict(x_train)
            self.log_metrics(model, self.config.metrics, y_train, y_pred)
            mlflow.end_run()
        except Exception as e:
            logger.error(e)
            raise e
    
    def save_model(self, model, path: str):
        try:
            mlflow.sklearn.save_model(model, path)
            logger.info("Model saved sucessfully")
        except Exception as e:
            logger.error("Error while saving model %s", e)
            raise e