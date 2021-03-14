import os

from functools import lru_cache

from pydantic import BaseSettings


path = os.path.dirname(os.path.realpath(__file__))


class Settings(BaseSettings):
    show_n_chars: int

    class Config:
        env_file = f'{path}/config.txt'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings():
    return Settings()
