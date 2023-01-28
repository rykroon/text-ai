import os
from starlette.config import Config


"""
    The default values are for production use.
    Use the 'GUNICORN_{}' environment variables to override the configuration.
    - See the following link for additional settings
    https://docs.gunicorn.org/en/stable/settings.html
"""
_config = Config()
DEBUG = _config.get('DEBUG', cast=bool, default=False)


bind            = _config.get('GUNICORN_BIND', default='0.0.0.0')
loglevel        = _config.get('GUNICORN_LOGLEVEL', default='debug' if DEBUG else 'info')
preload_app     = _config.get('GUNICORN_PRELOAD_APP', cast=bool, default=not DEBUG)
reload          = _config.get('GUNICORN_RELOAD', cast=bool, default=DEBUG)
workers         = _config.get('GUNICORN_WORKERS', cast=int, default=1 if DEBUG else os.cpu_count() * 2 + 1)
worker_class    = _config.get('GUNICORN_WORKER_CLASS', default='workers.RestartableUvicornWorker')
