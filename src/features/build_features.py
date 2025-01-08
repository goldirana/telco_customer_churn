from src import logger
from src.data.make_dataset import DataIngestion
from src.config.configuration import ConfigurationManager
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd
from src.utils.common import save_pickle, read_pickle, read_yaml
from src.constants import *
from dataclasses import dataclass
from box import ConfigBox
import numpy as np

logger.name = "Feature Enginnering"

class FeatureEnginnering:
    def __init__(self):
        pass
    
    def check_null(self, data:pd.DataFrame):
        try:
            if data.isnull().sum().sum() == 0:
                logger.debug("Data has no missing values")
            else:
                logger.warning("Data has missing values")
        except Exception as e:
            logger.error(e)
            raise e
            
    def fit_label_encoder(self, data: pd.DataFrame):
        fitter = {}
        columns = data.select_dtypes(object).columns
        for col in columns:
            le = LabelEncoder()
            try:
                assert data[col].isnull().sum() == 0, logger.warning(f"Missing values occured in {col}")
                fitter.update({col: le.fit(data[col])})
            except Exception as e:
                logger.error(e)
        return fitter

    def encoder_transform(self, encoder, data) -> pd.DataFrame:
        try:
            assert type(data) == pd.DataFrame, logger.error("Data not in pd.DataFrame func: encoder_transform")
            try:
                for col, ob in encoder.items():
                    assert data[col].isnull().sum() ==0, logger.warning(f"Missing values occured in {col}")
                    try:
                        data[col] = ob.transform(data[col])
                    except Exception as e:
                        logger.error(f"Error occured while converting data: {col}\n{encoder}")
                return data
            except Exception as e:
                logger.error(e)
                raise e
        except Exception as e:
            logger.error(e)
            raise e

    def fit_scalar(self, data:pd.DataFrame)-> object:
        ss = StandardScaler()
        try:
            ss.fit(data)
            logger.info("Standard Scalar fitted sucessfully")
            return ss
        except Exception as e:
            logger.error("Error occured while fitting standard scalar %s", e)

    def scalar_transform(self, scalar, data:pd.DataFrame)->pd.DataFrame:
        try:
            columns = data.columns
            data = scalar.transform(data)
            logger.info("Transformed data using standard scalar")
            return pd.DataFrame(data, columns=columns)
        except Exception as e:
            logger.error("Error occured while transforming standard scalar %s", e)
            raise e
        
    def drop_columns(self, data:pd.DataFrame, columns:list):
        try:
            data = data.drop(columns, inplace=False,axis=1)
            logger.info("Dropped columns: %s", columns)
            return data
        except:
            logger.error(f"Error occured while dropping columns: {columns}")
        