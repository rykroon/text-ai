import logging
from starlette.applications import Starlette
from routes import routes


app = Starlette(
    routes=routes
)


app.state.logger = logging.getLogger('gunicorn.error')
