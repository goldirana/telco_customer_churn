from sklearn.model_selection import train_test_split
from src.utils.common import read_yaml, create_directory
import pandas as pd
from src import logger
from pathlib import Path
from src.constants import *
from src.config.configuration import ConfigurationManager

STAGE_NAME = "Data Ingestion"
logger.name = STAGE_NAME

class DataIngestion:
    
    def __init__(self):
        pass
    
    def get_data(self, path)-> pd.DataFrame:
        try:
            df = pd.read_csv(path)
            logger.info("Data read sucessfully %s", path)
            return df
        except FileNotFoundError:
            logger.error("FileNotFoundError %s", path)
        except Exception as e:
            logger.error("Error occured while reading data: %s", e)
    
    def split_data(self, df: pd.DataFrame, test_size: float):
        """Used to split the data into train and test, if return_target is
        passed returns the target seprately

        Args:
            df (pd.DataFrame): original dataset
            test_size (float): how much percent to keep the test size
        """

        try:
            x, y = train_test_split(df, test_size=test_size, random_state=12)
            logger.info("Data splitted sucesssfully")
            return x, y
        except pd.errors.EmptyDataError as e:
            logger.error(e)
        except Exception as e:
            logger.error(e)

    def save_dataframe(self, data:pd.DataFrame, location: str):
        """Stores the dataframe to the given location in csv format

        Args:
            data (pd.DataFrame): data to be stored
            location (str): location with extension
        """
        try:
            location = str(Path(location).resolve())
            create_directory(location, is_extension_present=True)
            data.to_csv(location, index=False)
            logger.info("Data stored sucessfully at: %s", location)
        except Exception as e:
            logger.error(f"Error occured while saving data at: {location}\n {e}")
        
    def split_x_y(self, df:pd.DataFrame, target: str) -> tuple:
        """Splits the independent and target variable

        Args:
            df (pd.DataFrame): dataframe
            target (str): name of target variable

        Returns:
            tuple: (x: pd.DataFrame, y: pd.Series)
        """
        try:
            y = df.pop(target)
            logger.info("Splitted data into x and y sucessfully")
            return df, y
        except Exception as e:
            logger.error("Exception occured at splitting the data: %s", e)
    
