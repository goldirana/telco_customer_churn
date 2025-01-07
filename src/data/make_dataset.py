from sklearn.model_selection import train_test_split
from src import logger, read_yaml
import pandas as pd

logger.name = __name__


def split_data(df: pd.DataFrame, test_size: float):
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
        