import logging

from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.responses import Response
from starlette.routing import Route

from openai import create_completion, Gpt3Model
from telnyx import send_sms


async def root(request):
    return Response('OK')


class TelnyxWebhook(HTTPEndpoint):
    async def post(self, request):
        request_json = await request.json()
        data = request_json['data']
        event_type = data['event_type']
        payload = data['payload']

        match event_type.split('.'):
            case 'message', 'received':
                await self._message_received(request, payload)

            case _:
                ...
        
        return Response('OK')
    
    async def _message_received(self, request, payload):
        from_ = payload['from']['phone_number']
        to = payload['to'][0]['phone_number']
        text = payload['text']

        result = await create_completion(
            model=Gpt3Model.DAVINCI,
            prompt=text,
            max_tokens=32
        )
        gpt_text = result['choices'][0]['text']
        await send_sms(from_=to, to=from_, text=gpt_text)


app = Starlette(
    routes=[
        Route('/', root, methods=['GET']),
        Route('/telnyx', TelnyxWebhook, methods=['POST'])
    ]
)
