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
    encoder_dir: str