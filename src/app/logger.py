import logging
import os

logging.config.fileConfig(
    os.path.join('src', 'logging.conf'),
    disable_existing_loggers=False)


def get_logger(__name__) -> logging.Logger:

    return logging.getLogger(_logger_name(__name__))


def _logger_name(name):
    words = name.split('.')
    if len(words) == 1:
        return name
    words = words[1:]
    if words[0] == 'services':
        words[0] = 'SRV'
    elif words[0] == 'repositories':
        words[0] = 'REP'
    elif words[0] == 'app':
        words[0] = 'APP'
    return '.'.join(words)
