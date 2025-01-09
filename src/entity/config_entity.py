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
    target_encoder_dir: str

@dataclass(frozen=True)
class ModelBuildingConfig:
    model_dir: str
    sub_module: str
    model_name: str
    train_dir: str
    target_col: str
    experiment_name: str
    metrics: list
    save_model_path: str
    model_params: dict
    
@dataclass
class ModelEvaluationConfig:
    saved_model_dir: str
    test_dir: str
    metrics: list
    target_col: str
    experiment_name: str