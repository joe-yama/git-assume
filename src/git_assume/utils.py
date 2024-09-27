import logging
import logging.config
import sys

import yaml


def ask(question: str, include_guide: bool = True) -> bool | None:
    dic = {"": True, "y": True, "yes": True, "n": False, "no": False}
    if include_guide:
        question += " [Y/n] "
    ans = input(question).lower()
    return dic.get(ans, None)


def setup_logger(logger_configfile_path: str):
    with open(logger_configfile_path, "r") as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
