from sanic import Blueprint
from sanic.exceptions import Unauthorized
from sanic.log import logger
from sanic import response
from sanic.views import HTTPMethodView

from services.telnyx import verify_signature, InvalidTelnyxSignature
from tasks import create_text_completion_and_send_message, create_image_and_send_message, \
    create_chat_completion_and_send_message
from models import User, AccessNumber


bp = Blueprint("telnyx")


@bp.middleware
async def verify_webhook(request):
    if 'telnyx-signature-ed25519' not in request.headers:
        raise Unauthorized

    if 'telnyx-timestamp' not in request.headers:
        raise Unauthorized

    signature = request.headers['telnyx-signature-ed25519'].encode()
    timestamp = request.headers['telnyx-timestamp'].encode()

    try:
        verify_signature(
            signature,
            timestamp,
            request.body,
            tolerance=60*5
        )
    
    except InvalidTelnyxSignature:
        raise Unauthorized


class TelnyxWebhook(HTTPMethodView):

    async def post(self, request):
        event_type = request.json['data']['event_type']

        match event_type.split('.'):
            case 'message', 'received':
                await self._message_received(request)

            case 'message', 'sent':
                await self._message_sent(request)

            case 'message', 'finalized':
                await self._message_finalized(request)
            
            case _:
                logger.warning(f"Unhandled event '{event_type}'.")

        return response.text('OK')

    async def _message_sent(self, request):
        # The message was sent by Telnyx.
        logger.debug("Message sent.")

    async def _message_finalized(self, request):
        # The message delivery was confirmed.
        logger.debug("Message delivered.")

    async def _message_received(self, request):
        logger.debug('Message received.')
        payload = request.json['data']['payload']

        from_ = payload['from']['phone_number']
        to = payload['to'][0]['phone_number']
        text = payload['text']

        # future checks
        # check to do proper rate limiting depending on the status of the sender.
        # check to make sure the text does not contain anything inapropriate

        user = await User.find_one(phone_number=from_)
        if user is None:
            logger.debug(f"Phone number '{from_}' does not have access.")
            return

        access_number = await AccessNumber.find_one(phone_number=to)
        if access_number is None:
            return

        match access_number.service:
            case 'openai.chat-completion':
                coroutine = create_chat_completion_and_send_message(
                    user_uuid=user.uuid,
                    message_content=text,
                    from_=to,
                    to=from_
                )

            case 'openai.text-completion':
                coroutine = create_text_completion_and_send_message(
                    prompt=text,
                    from_=to,
                    to=from_
                )

            case 'openai.image-generation':
                coroutine = create_image_and_send_message(
                    prompt=text,
                    from_=to,
                    to=from_
                )

            case _:
                return
        
        request.app.add_task(coroutine)


bp.add_route(TelnyxWebhook.as_view(), '/telnyx', name='TelnyxWebhook')
