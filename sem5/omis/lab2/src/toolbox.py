import os
import logging
import psycopg2
from dotenv import load_dotenv


load_dotenv()


def get_logger(filename: str = None) -> logging.Logger:
    if not filename:
        filename = 'application.log'
    logger_ = logging.getLogger(filename)
    if not logger_.handlers:
        logger_.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(f"{filename}")
        file_handler.setLevel(logging.WARNING)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        logger_.addHandler(file_handler)
        logger_.addHandler(stream_handler)
    return logger_


logger = get_logger()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("SERVICE_PORT", 5432),
}

def get_psycopg_conn():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        return None