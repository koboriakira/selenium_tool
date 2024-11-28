import logging
import os
from logging import Logger


def get_logger(name: str | None) -> Logger:
    logger = logging.getLogger(name)  # logger名loggerを取得

    if os.getenv("IS_DEBUG") == "true":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # handler1: 標準出力
    handler1 = logging.StreamHandler()
    handler1.setFormatter(logging.Formatter("%(asctime)s %(levelname)8s %(message)s"))
    logger.addHandler(handler1)

    return logger
