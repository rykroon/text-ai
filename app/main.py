import logging
from starlette.applications import Starlette
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings
from starlette.middleware import Middleware
from starlette.responses import Response
from starlette.routing import Route

from middleware import ReplayableReceiveMiddleware
from routes import TelnyxWebhook


config = Config()


routes = [
    Route('/telnyx', TelnyxWebhook, methods=['POST'])
]


app = Starlette(
    routes=routes,
    middleware=[
        Middleware(ReplayableReceiveMiddleware)
    ]
)

@app.route('/', methods=['GET'])
async def homepage(request):
    request.app.state.logger.debug('Debug is turned on.')
    await request.body()
    return Response('OK')


app.state.logger = logging.getLogger('gunicorn.error')
app.state.white_list = config.get('WHITE_LIST', cast=CommaSeparatedStrings)
