import logging

from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.responses import Response
from starlette.routing import Route

from services.openai import create_completion, Gpt3Model, create_image, ImageSize
from services.telnyx import send_sms


async def root(request):
    return Response('OK')


async def telnyx_webhook(request) -> Response:
    request_json = await request.json()
    data = request_json['data']
    event_type = data['event_type']
    payload = data['payload']

    match event_type.split('.'):
        case 'message', 'received':
            return await _message_received(request, payload)

        case 'message', 'sent':
            ...

        case 'message', 'finalized':
            ...

    request.app.state.logger.warning(event_type)
    return Response('OK')


async def _message_received(request, payload) -> Response:
    from_ = payload['from']['phone_number']
    to = payload['to'][0]['phone_number']
    text = payload['text']

    # future checks
    # check to make sure that sender is a customer.
    # check to do proper rate limiting depending on the status of the sender.
    # check to make sure if the number should do text completion or image creation.
    # check to make sure the text does not contain anything inapropriate

    task = BackgroundTask(
        _create_image_and_send_sms,
        prompt=text,
        from_=to,
        to=from_
    )

    return Response('OK', background=task)


async def _create_image_and_send_sms(prompt: str, from_: str, to: str):
    result = await create_image(
        prompt=prompt,
        size=ImageSize.SMALL
    )
    url = result['data'][0]['url']
    await send_sms(from_=from_, to=to, text="", media_urls=[url])


async def _create_completion_and_send_sms(prompt: str, from_: str, to: str):
    result = await create_completion(
        model=Gpt3Model.CURIE,
        prompt=prompt,
        max_tokens=64
    )
    text = result['choices'][0]['text']
    await send_sms(from_=from_, to=to, text=text)


app = Starlette(
    routes=[
        Route('/', root, methods=['GET']),
        Route('/telnyx', telnyx_webhook, methods=['POST'])
    ]
)


app.state.logger = logging.getLogger('gunicorn.error')