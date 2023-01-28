import logging
from starlette.applications import Starlette
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings
from routes import routes


config = Config()


app = Starlette(
    routes=routes
)


app.state.logger = logging.getLogger('gunicorn.error')
app.state.white_list = config.get('WHITE_LIST', cast=CommaSeparatedStrings)
