"""The job of this file is read all the raw data from different sources and converting
into entities defined in entity/config_entity.py. instead of reading data in each module this 
serves the purpose and reduces the complexity of reading files. This is also helpful as the complexity 
of the project grows and you require more parameters"""

from src.constants import *
from src import logger
from src.utils.common import read_yaml
from src.entity.config_entity import (DataIngestionConfig,
                                      FeatureEngineeringConfig,
                                      ModelBuildingConfig,
                                      ModelEvaluationConfig,
                                      DagsHubConfig)

logger.name = "Configuration Manager"

class ConfigurationManager:
    def __init__(self,
        config_file_path=CONFIG_FILE_PATH,
        params_file_path=PARAMS_FILE_PATH):
        self.config = read_yaml(config_file_path)
        # print(self.config)
        self.params = read_yaml(params_file_path)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        data_ingestion_config = DataIngestionConfig(
            root_dir=self.config.data_directory.root_dir,
            train_dir=self.config.data_directory.interim_train,
            test_dir=self.config.data_directory.interim_test,
            test_size=self.params.make_dataset.test_size)
        return data_ingestion_config

    def get_feature_engineering_config(self)-> FeatureEngineeringConfig:
        feature_engineering_conf = FeatureEngineeringConfig(
            train_dir = str(Path(self.config.data_directory.interim_train)),
            test_dir = str(Path(self.config.data_directory.interim_test)),
            encoder_dir=self.config.artifacts.encoder,
            scalar_dir=self.config.artifacts.scalar,
            target_col=self.params.data.target_col,
            drop_cols=self.params.data.drop_columns,
            processed_train=str(Path(self.config.data_directory.processed_train).resolve()),
            processed_test=str(Path(self.config.data_directory.processed_test).resolve()),
            col_names_to_save=self.config.artifacts.col_names_to_save,
            target_encoder_dir=self.config.artifacts.target_encoder_dir
        )
        return feature_engineering_conf
    
    def get_model_building_config(self)-> ModelBuildingConfig:
        model_args_name = self.params.model.model_args_name
        model_building_conf = ModelBuildingConfig(
            model_dir=self.config.model.root_dir,
            sub_module=self.params.model.sub_model,
            model_name=self.params.model.model_name,
            train_dir=self.config.data_directory.processed_train,
            target_col=self.params.data.target_col,
            experiment_name=self.params.model.experiment_name,
            parent_run_dir=self.config.artifacts.parent_run_dir,
            metrics=self.params.model.metrics,
            save_model_path=self.config.model.root_dir,
            model_params=self.params.model_params[model_args_name])
        return model_building_conf
    
    def get_evaluation_config(self)-> ModelEvaluationConfig:
        model_evaluator_config = ModelEvaluationConfig(
        saved_model_dir=self.config.model.saved_model,
        test_dir=str(Path(self.config.data_directory.processed_test).resolve()),
        metrics=self.params.model.metrics,
        target_col=self.params.data.target_col,
        experiment_name=self.params.model.experiment_name,
        parent_run_dir=self.config.artifacts.parent_run_dir)
        return model_evaluator_config

    def get_dagshub_config(self)-> DagsHubConfig:
        dagshub_config=DagsHubConfig(
            repo_owner=self.config.dags_hub.repo_owner,
            repo_name=self.config.dags_hub.repo_name,
            tracking_ui=self.config.dags_hub.tracking_ui
        )
        return dagshub_config   
    

if __name__ == "__main__":
    config_manager = ConfigurationManager()
    print(config_manager.params)
    model_args_name=config_manager.params.model.model_args_name
    model_params=config_manager.params.model_params[model_args_name]
    print(model_args_name)
    print(model_params)
    print(config_manager.get_evaluation_config())
    print("--"*30)
    print(config_manager.get_model_building_config())
    print("---"*45)
    print(config_manager.get_dagshub_config())