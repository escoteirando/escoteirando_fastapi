import glob
import importlib
import os

from src.app import get_logger

logger = get_logger(__name__)


def import_controllers():
    controllers_path = os.path.join(
        os.path.dirname(__file__), '*_controller.py')
    loading_modules = [
        'src.middleware.authorization_middleware'
    ]

    for module in glob.glob(controllers_path):
        loading_modules.append(
            'src.controllers.'+os.path.splitext(os.path.basename(module))[0])

    modules = []
    for module in loading_modules:
        try:
            importlib.import_module(module)
            modules.append(os.path.basename(module))
        except Exception as exc:
            logger.error('ERROR WHEN LOADING CONTROLLER %s: %s',
                         module, str(exc))
            return False

    logger.info("CONTROLLERS: %s", modules)
    return True
