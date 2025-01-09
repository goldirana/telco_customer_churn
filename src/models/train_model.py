#!/usr/bin/env python
from src.utils.common import read_pickle, read_yaml, read_array, read_json
from src.data.make_dataset import DataIngestion
from src.constants import *
from src import logger
from dataclasses import dataclass
from box import ConfigBox
from typing import Optional
from src.config.configuration import ModelBuildingConfig, DagsHubConfig

# model building
import sklearn as sk
from importlib import import_module
import mlflow, json
import sys
import dagshub

STAGE_NAME = "STAGE 2: MODEL BUILDING"
logger.name = STAGE_NAME

def get_experiment_name_and_id(path_to_json):
    params = read_json(path_to_json)
    experiment_name = params["experiment_id"]
    run_id = params["run_id"]
    return {"experiment_id": experiment_name, 
            "run_id": run_id}

class BuildModel:
    def __init__(self, config: ModelBuildingConfig,
                 dags_hub_config: DagsHubConfig):
        
        self.config = config
        self.dags_config = dags_hub_config

        dagshub.init(repo_owner=self.dags_config.repo_owner,
                     repo_name=self.dags_config.repo_name, 
                     mlflow=True)

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
        mlflow.end_run()
        mlflow.set_tracking_uri(self.dags_config.tracking_ui)
        try:
            try: # to get the tracking parameters
                tracking_params = get_experiment_name_and_id(self.config.parent_run_dir)
                logger.info("Tracking parameters read sucessfully")
            except Exception as e:
                logger.error("Error occured while reading tracking paramters")
                raise e
        
            if data_name != "Train": 
                mlflow.set_experiment(experiment_id = tracking_params["experiment_id"])
                mlflow.start_run(experiment_id = tracking_params["experiment_id"],
                                run_id=tracking_params["run_id"],
                                nested=True)
            else:
                mlflow.set_experiment(self.config.experiment_name)
                mlflow.start_run(experiment_id = tracking_params["experiment_id"],
                                run_id=tracking_params["run_id"])
                
                
            for metric in metrics:
                module = import_module("sklearn.metrics")
                metric_func = getattr(module, metric)
                mlflow.log_metric(data_name +" "+ metric_func.__name__, metric_func(y_true, y_pred))
            
            logger.info("Metrics logged sucessfully")
            mlflow.end_run()
        except Exception as e:
            logger.error(e)
            raise e
        
    def record_mlflow_params(self, data, path_to_json: str):
        try:
            with open(path_to_json, "w") as f:
                json.dump(data, f)
            logger.info(f"Mlflow parameters saved at: {path_to_json}")
        except Exception as e:
            logger.error(e)
        
    def fit(self, x_train, y_train):
        try:
            model = self.get_model_class()
            # initiating model
            mlflow.set_tracking_uri(self.dags_config.tracking_ui)
            mlflow.set_experiment(self.config.experiment_name)
            mlflow.start_run()
            
            # to save the active run parameters            
            self.record_mlflow_params(dict(mlflow.active_run().info), self.config.parent_run_dir)

            mlflow.log_params(self.config.model_params)

            model = model(**self.config.model_params)
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