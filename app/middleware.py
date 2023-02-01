
from starlette.responses import Response
from starlette.requests import Request, ClientDisconnect
import logging


logger = logging.getLogger('gunicorn.error')

class ReplayableReceiveMiddleware:

    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        new_receive = ReplayableReceive(receive)

        logger.debug(f'{new_receive.consumed=}')
        logger.debug(f'{new_receive.disconnected=}')

        request = Request(scope, new_receive, send)
        await request.body()

        logger.debug(f'{new_receive.consumed=}')
        logger.debug(f'{new_receive.disconnected=}')

        # ------

        response = Response("OK")
        await response(scope, new_receive, send)

        # -----

        logger.debug(f'{new_receive.consumed=}')
        logger.debug(f'{new_receive.disconnected=}')

        new_receive.restart()
        await self.app(scope, new_receive, send)


class ReplayableReceive:

    def __init__(self, receive):
        self.receive = receive
        self.messages = []
        self.index = -1
        self.consumed = False
        self.disconnected = False

    async def __call__(self):
        logger.debug('__call__')
        self.index += 1
        try:
            return self.messages[self.index]

        except IndexError:
            return await self._call_original_receive()

    def restart(self):
        self.index = -1
    
    async def _call_original_receive(self):
        logger.debug('_call_original_receive')
        message = await self.receive()
        self.messages.append(message)
        self.index += 1
    
        if message['type'] == 'http.request':
            more_body = message.get('more_body', False) 
            self.consumed = not more_body

        if message['type'] == 'http.disconnect':
            self.disconnected = True

        return message
