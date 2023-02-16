from sanic import Blueprint
from sanic.exceptions import Unauthorized
from sanic.log import logger
from sanic.response import text
from sanic.views import HTTPMethodView

from services.telnyx import verify_signature
from tasks import create_completion_and_send_message, create_image_and_send_message


bp = Blueprint("my_blueprint")


@bp.get('/')
async def homepage(request):
    logger.debug('Debug is turned on.')
    return text("OK")


class TelnyxWebhook(HTTPMethodView):

    async def post(self, request):
        if not await self._verify_webhook(request):
            raise Unauthorized

        request_json = await request.json()
        data = request_json['data']
        event_type = data['event_type']
        payload = data['payload']

        match event_type.split('.'):
            case 'message', 'received':
                return await self._message_received(request, payload)

            case 'message', 'sent':
                return await self._message_sent(request, payload)

            case 'message', 'finalized':
                return await self._message_finalized(request, payload)

        request.app.state.logger.warning(f"{event_type=}")
        return text('OK')

    async def _verify_webhook(self, request) -> bool:
        if 'telnyx-signature-ed25519' not in request.headers:
            return False

        if 'telnyx-timestamp' not in request.headers:
            return False

        signature = request.headers['telnyx-signature-ed25519'].encode()
        timestamp = request.headers['telnyx-timestamp'].encode()
        content = await request.body()

        if not verify_signature(signature, timestamp, content, tolerance=60*5):
            return False

        return True

    async def _message_sent(self, request, payload):
        # The message was sent by Telnyx.
        logger.debug("Message sent.")
        return text("OK")

    async def _message_finalized(self, request, payload):
        # The message delivery was confirmed.
        logger.debug("Message delivered.")
        return text("OK")

    async def _message_received(self, request, payload):
        logger.debug('Message received.')

        from_ = payload['from']['phone_number']
        to = payload['to'][0]['phone_number']
        text = payload['text']

        # future checks
        # check to make sure that sender is a customer.
        # check to do proper rate limiting depending on the status of the sender.
        # check to make sure if the number should do text completion or image creation.
        # check to make sure the text does not contain anything inapropriate

        # check white list to see if the sender is allowed to use the service.
        if from_ not in request.app.ctx.white_list:
            return text('OK')

        await create_completion_and_send_message(
            prompt=text,
            from_=to,
            to=from_
        )

        return text('OK')


bp.add_route(TelnyxWebhook.as_view(), '/telnyx')