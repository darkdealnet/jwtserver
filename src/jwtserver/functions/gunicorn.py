from multiprocessing import cpu_count
from os import getenv
from jwtserver.functions.config import load_config

config = load_config()


def max_workers():
    return cpu_count()


host = getenv('APP', 'localhost')

bind = f'{host}:8080'
max_requests = 1000
worker_class = 'uvicorn.workers.UvicornWorker'
workers = max_workers()
threads = max_workers() * 2

reload = True
name = 'troll'
