import time

from starlette.background import BackgroundTask
from starlette.endpoints import HTTPEndpoint
from starlette.responses import Response

from services.telnyx import verify_signature
from tasks import create_completion_and_send_message, create_image_and_send_message


async def homepage(request):
    request.app.state.logger.debug('Debug is turned on.')
    return Response('OK')


class TelnyxWebhook(HTTPEndpoint):

    async def post(self, request) -> Response:
        if not await self._verify_webhook(request):
            return Response(status_code=401)
    
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
        return Response('OK')
    
    async def _verify_webhook(self, request):
        if 'telnyx-signature-ed25519' not in request.headers:
            return False

        if 'telnyx-timestamp' not in request.headers:
            return False

        signature = request.headers['telnyx-signature-ed25519'].encode()
        timestamp = request.headers['telnyx-timestamp'].encode()
        content = await request.body()

        if not verify_signature(signature, timestamp, content):
            return False

        tolerance = 60*5 # Five minutes.
        if int(timestamp) < time.time() - tolerance:
            return False
        
        return True

    async def _message_sent(self, request, payload) -> Response:
        # The message was sent by Telnyx.
        request.app.state.logger.debug("Message sent.")
        return Response("OK")

    async def _message_finalized(self, request, payload) -> Response:
        # The message delivery was confirmed.
        request.app.state.logger.debug("Message delivered.")
        return Response("OK")

    async def _message_received(self, request, payload) -> Response:
        request.app.state.logger.debug('Message received.')

        from_ = payload['from']['phone_number']
        to = payload['to'][0]['phone_number']
        text = payload['text']

        # future checks
        # check to make sure that sender is a customer.
        # check to do proper rate limiting depending on the status of the sender.
        # check to make sure if the number should do text completion or image creation.
        # check to make sure the text does not contain anything inapropriate

        # check white list to see if the sender is allowed to use the service.
        if from_ not in request.app.state.white_list:
            return Response('OK')

        task = BackgroundTask(
            create_completion_and_send_message,
            prompt=text,
            from_=to,
            to=from_
        )

        return Response('OK', background=task)
