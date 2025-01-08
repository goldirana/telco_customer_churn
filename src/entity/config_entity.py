from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir:str
    train_dir: str
    test_dir: str
    test_size: float