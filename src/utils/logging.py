import logging


def setup_logger() -> logging.Logger:
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y-%H:%M:%S')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger
