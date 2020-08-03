import logging
import os
import tempfile


def setup_log():
    log_level = os.getenv('LOG_LEVEL', 'DEBUG')
    config_file = os.path.join('src', 'logging.conf')
    with open(config_file) as f:
        config_setup = f.read()

    if log_level != 'DEBUG':
        config_setup = config_setup.replace('DEBUG', log_level)

    with tempfile.NamedTemporaryFile(mode='w') as f:
        f.write(config_setup)
        f.flush()
        logging.config.fileConfig(
            f.name,
            disable_existing_loggers=False)

    get_logger(__name__).info('INIT LOGGING [LEVEL=%s]', log_level)


def get_logger(name) -> logging.Logger:
    return logging.getLogger(_logger_name(name))


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


setup_log()
