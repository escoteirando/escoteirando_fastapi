from config_guiosoft import ConfigClass


class Config(ConfigClass):
    MONGODB_URI = ''
    MONGODB_DATABASE = 'escoteirando'
    AUTHORIZATION_TTL: int = 604800  # 7 DIAS

    MAILER_SMTP_HOST = 'smtp.gmail.com'
    MAILER_SMTP_PORT = 465
    MAILER_SMTP_USER = 'guionardo@gmail.com'
    MAILER_SMTP_PASS = 'pbsgtevdnzqsovmn'
    MAILER_SMTP_SSL = True
    MAILER_SENDER_EMAIL = 'guionardo@gmail.com'
    MAILER_SENDER_NAME = 'Guionardo Furlan'
    MAILER_THROTTLE = 50    # 50 emails por hora

    CACHE_CONFIG = 'sqlite://.cache.sqlite'

    BACKEND_HOST = 'http://localhost'
    BACKEND_PORT = 8000
    FRONTEND_PORT = 8080
