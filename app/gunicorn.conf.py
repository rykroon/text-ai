import os

"""
    The default values are for production use.
    Use the 'GUNICORN_{}' environment variables to override the configuration.
    - See the following link for additional settings
    https://docs.gunicorn.org/en/stable/settings.html
"""


bind            = os.getenv('GUNICORN_BIND', '0.0.0.0')
loglevel        = os.getenv('GUNICORN_LOGLEVEL', 'info')
preload_app     = os.getenv('GUNICORN_PRELOAD_APP', True)
reload          = os.getenv('GUNICORN_RELOAD', False)
workers         = os.getenv('GUNICORN_WORKERS', 1)
worker_class    = os.getenv('GUNICORN_WORKER_CLASS', 'uvicorn.workers.UvicornWorker')
