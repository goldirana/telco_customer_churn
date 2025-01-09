#!/usr/bin/env python

from src.models.predict_model import ModelEvaluation
from src.config.configuration import ConfigurationManager
from src.data.make_dataset import DataIngestion
from src import logger
import mlflow


STAGE_NAME = "STAGE 3: MODEL EVALUATION"
logger.name = STAGE_NAME


class ModelEvaluationPipeline:
    def __init__(self):
        pass

    def main(self):
        config_manager = ConfigurationManager()
        config_params = config_manager.get_evaluation_config()
        dags_params = config_manager.get_dagshub_config()

        model_evaluator = ModelEvaluation(config_params,
                                          dags_params)
        data_ingestion = DataIngestion()

        test = data_ingestion.get_data(config_params.test_dir)
        x_test, y_test = data_ingestion.split_x_y(test, config_params.target_col)

        model = model_evaluator.load_model()
        model_evaluator.evaluate(model, x_test, y_test)

if __name__ == "__main__":
    try:
        logger.info(f">>>>>> Train {STAGE_NAME} started <<<<<<")
        obj = ModelEvaluationPipeline()
        obj.main()
        logger.info(f">>>>>> Train {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.error(e)
        raise e

