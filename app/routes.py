from starlette.background import BackgroundTask
from starlette.endpoints import HTTPEndpoint
from starlette.responses import Response
from starlette.routing import Route

from services.openai import create_completion, create_image, ImageSize, Gpt3Model
from services.telnyx import send_sms


async def root(request):
    return Response('OK')


class TelnyxWebhook(HTTPEndpoint):

    async def post(self, request) -> Response:
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

    async def _message_sent(self, request, payload) -> Response:
        # The message was sent by Telnyx.
        request.app.state.logger.warning(payload)
        return Response("OK")

    async def _message_finalized(self, request, payload) -> Response:
        # The message delivery was confirmed.
        request.app.state.logger.warning(payload)
        return Response("OK")

    async def _message_received(self, request, payload) -> Response:
        from_ = payload['from']['phone_number']
        to = payload['to'][0]['phone_number']
        text = payload['text']

        # future checks
        # check to make sure that sender is a customer.
        # check to do proper rate limiting depending on the status of the sender.
        # check to make sure if the number should do text completion or image creation.
        # check to make sure the text does not contain anything inapropriate

        task = BackgroundTask(
            _create_completion_and_send_sms,
            prompt=text,
            from_=to,
            to=from_
        )

        return Response('OK', background=task)


routes = [
    Route('/', root, methods=['GET']),
    Route('/telnyx', TelnyxWebhook, methods=['POST'])
]


# ~~~ Background Tasks ~~~

async def _create_image_and_send_sms(prompt: str, from_: str, to: str):
    result = await create_image(
        prompt=prompt,
        size=ImageSize.SMALL
    )
    url = result['data'][0]['url']
    await send_sms(from_=from_, to=to, text="", media_urls=[url])


async def _create_completion_and_send_sms(prompt: str, from_: str, to: str):
    result = await create_completion(
        model=Gpt3Model.DAVINCI,
        prompt=prompt,
        max_tokens=64
    )
    text = result['choices'][0]['text']
    await send_sms(from_=from_, to=to, text=text)