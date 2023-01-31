import logging
from starlette.applications import Starlette
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings
from starlette.routing import Route

from routes import homepage, TelnyxWebhook


config = Config()


routes = [
    Route('/', homepage, methods=['GET']),
    Route('/telnyx', TelnyxWebhook, methods=['POST'])
]


app = Starlette(
    routes=routes
)


app.state.logger = logging.getLogger('gunicorn.error')
app.state.white_list = config.get('WHITE_LIST', cast=CommaSeparatedStrings)
