import configparser
import importlib.resources as pkg_resources
from collections import defaultdict
from typing import Optional
from pydantic import BaseModel

import jwtserver


class TokenConfig(BaseModel):
    sol: str
    secret_key: str
    algorithm: str
    access_expire_time: int
    refresh_expire_time: int


class DbConfig(BaseModel):
    sync_url: str
    async_url: str
    sync_test_url: Optional[str] = None
    async_test_url: Optional[str] = None


class RedisConfig(BaseModel):
    url: str
    max_connections: int


class GoogleConfig(BaseModel):
    secret_key: str


class SMSConfig(BaseModel):
    debug = True
    provider: str
    init_class: str
    login: str
    password: str
    time_sms: int
    time_call: int


class ServerConfig(BaseModel):
    host: str
    port: str
    max_requests: int
    debug: bool
    clear_redis_before_send_code: bool


class Config(BaseModel):
    server: ServerConfig
    token: TokenConfig
    db: DbConfig
    redis: RedisConfig
    google: GoogleConfig
    sms: SMSConfig


def load_config() -> Config:
    """
    Load default and user config. Merge configs (override default values) and typing.
    :return: merge configs.
    :rtype: Config.
    """

    # Load default.ini file and parsing.
    default_ini = pkg_resources.open_text(jwtserver, 'default.ini')
    default_cfg = configparser.ConfigParser()
    default_cfg.read_file(default_ini)

    # Load config.ini file (User config) and parsing.
    user_ini = configparser.ConfigParser()
    user_ini.read('config.ini')

    # Merge dicts.
    merged_dict = defaultdict(dict)
    merged_dict.update(default_cfg)

    for key, nested_dict in user_ini.items():
        merged_dict[key].update(nested_dict)

    return Config(**dict(merged_dict))
