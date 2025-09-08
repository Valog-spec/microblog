import logging
import logging.config

from app.core.logging_config import dict_config


def get_logger(name: str) -> logging.Logger:
    """
    Создает и возвращает логгер с заданным именем, используя предустановленную конфигурацию

    Args:
        name (str): Имя логгера.
    Returns:
        Logger: Объект логгера, настроенный согласно конфигурации dict_config.
    """
    logging.config.dictConfig(dict_config)
    return logging.getLogger(name)
