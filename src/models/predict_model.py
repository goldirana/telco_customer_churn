from src.config.configuration import ConfigurationManager
from src.data.make_dataset import DataIngestion
from src.models.train_model import BuildModel
from src.entity.config_entity import ModelEvaluationConfig, DagsHubConfig
from src import logger
import mlflow
import dagshub

class ModelEvaluation(BuildModel):
    def __init__(self, config: ModelEvaluationConfig,
                        dags_hub_config: DagsHubConfig):
        self.config = config
        self.dags_config = dags_hub_config

        dagshub.init(repo_owner=self.dags_config.repo_owner,
                     repo_name=self.dags_config.repo_name, mlflow=True)

    def load_model(self):
        try:
            mlflow.set_experiment(self.config.experiment_name)
            model = mlflow.sklearn.load_model(self.config.saved_model_dir)
            logger.info("Model load sucessfully")
            return model
        except FileNotFoundError as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)
    
    def evaluate(self, model, x, y_true):
        try:
            prediction = model.predict(x)
            self.log_metrics(model, self.config.metrics, y_true, prediction, data_name="Test")
        except Exception as e:
            logger.error(e)
            raise e