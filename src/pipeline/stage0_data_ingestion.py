from src import logger
from src.data.make_dataset import DataIngestion
from src.config.configuration import ConfigurationManager

STAGE_NAME = "STAGE 0: DATA INGESTION"
logger.name = STAGE_NAME

class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
        data_ingestion = DataIngestion()
        config_manager = ConfigurationManager()
        data_ingestion_params = config_manager.get_data_ingestion_config()
        df = data_ingestion.get_data(data_ingestion_params.root_dir)
        train, test = data_ingestion.split_data(df, data_ingestion_params.test_size)
        data_ingestion.save_dataframe(train, data_ingestion_params.train_dir)
        data_ingestion.save_dataframe(test, data_ingestion_params.test_dir)


if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataIngestionPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.error(e)
        raise e