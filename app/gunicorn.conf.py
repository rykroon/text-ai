import os

"""
    The default values are for production use.
    Use the 'GUNICORN_{}' environment variables to override the configuration.
    - See the following link for additional settings
    https://docs.gunicorn.org/en/stable/settings.html
"""

DEBUG = False

bind            = os.getenv('GUNICORN_BIND', '0.0.0.0')
loglevel        = 'debug' if DEBUG else 'info'
preload_app     = False if DEBUG else True
reload          = True if DEBUG else False
workers         = os.getenv('GUNICORN_WORKERS', 1)
worker_class    = os.getenv('GUNICORN_WORKER_CLASS', 'workers.RestartableUvicornWorker')
