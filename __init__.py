import logging, os

from .config import Config
from .__version__ import __version__
from . import run

_levels = {
    'info': logging.INFO,
    'debug': logging.DEBUG
}

_level = os.getenv('TWINT_DEBUG', 'info')
_logLevel = _levels[_level]

if _level == "debug":
    logger = logging.getLogger()
    _output_fn = 'twint.log'
    logger.setLevel(_logLevel)
    formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')
    fileHandler = logging.FileHandler(_output_fn)
    fileHandler.setLevel(_logLevel)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
© 2021 GitHub, Inc.
Terms
Privacy
Security
Stat
