"""This is the file where you define your all entities that are required by each module"""
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir:str
    train_dir: str
    test_dir: str
    test_size: float


@dataclass(frozen=True)
class FeatureEngineeringConfig:
    train_dir: str
    test_dir: str
    encoder_dir: str
    scalar_dir: str
    target_col: str
    drop_cols: list
    processed_train: str
    processed_test: str
    col_names_to_save: str