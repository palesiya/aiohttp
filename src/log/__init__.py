import yaml
import logging
import logging.config as logconf
import pathlib


def initial_logging():
    with open(pathlib.Path(__file__).parent / "logging.yaml", "r") as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)


class Log:
    ...
