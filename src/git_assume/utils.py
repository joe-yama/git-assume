import logging
import logging.config
import sys

import yaml


def ask(question: str, include_guide: bool = True) -> bool | None:
    dic = {"y": True, "yes": True, "n": False, "no": False}
    if include_guide:
        question += " [Y]es/[N]o >> "
    ans = input(question).lower()
    return dic.get(ans, None)


def get_legacy_logger(level: str) -> logging.Logger:
    logger = logging.getLogger("git-assume")
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
    stdout_handler.setLevel(getattr(logging, level))
    logger.addHandler(stdout_handler)
    logger.setLevel(level)
    return logger


def setup_logger(logger_configfile_path: str, level: str):
    with open(logger_configfile_path, "r") as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
