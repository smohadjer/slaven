import logging


def logging_service() -> None:
    logger = logging.getLogger('root')
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(module)s:%(funcName)s():%(lineno)d | %(message)s')
    console_handler = logging.StreamHandler()

    logger.setLevel("INFO")
    console_handler.setLevel("INFO")

    logger.addHandler(console_handler)
    console_handler.setFormatter(formatter)
