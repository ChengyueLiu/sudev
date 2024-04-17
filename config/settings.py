import multiprocessing
import sys

from environs import Env
from loguru import logger

# ENV
env = Env()
env.read_env()

# Log
LOG_LEVEL = env.str("LOG_LEVEL", "INFO")
logger.remove()
logger.add(sys.stdout, level=LOG_LEVEL)

# Multiprocessing
POOL_SIZE = env.int("POOL_SIZE", multiprocessing.cpu_count())
