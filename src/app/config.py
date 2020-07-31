from config_guiosoft import ConfigClass


class Config(ConfigClass):
    MONGODB_URI = ''
    MONGODB_DATABASE = 'escoteirando'
    AUTHORIZATION_TTL: int = 604800  # 7 DIAS
