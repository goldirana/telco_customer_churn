from pathlib import Path

root_dir = str(Path(__name__).resolve().parent)

CONFIG_FILE_PATH = str(Path(root_dir +"/config/config.yaml"))
PARAMS_FILE_PATH = str(Path(root_dir + "/params.yaml"))