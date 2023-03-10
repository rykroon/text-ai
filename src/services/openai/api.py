import os
import httpx
from typing import Literal

from .enums import Gpt3Model, ImageSize
from .exceptions import OpenAiException
from .types import Message


API_KEY = os.environ['OPENAI_API_KEY']


client = httpx.AsyncClient(
    base_url="https://api.openai.com",
    headers={'Authorization': f"Bearer {API_KEY}"},
    http2=True
)


async def list_models():
    """
        https://platform.openai.com/docs/api-reference/models/list
    """
    return await client.get('v1/models')
 

async def create_text_completion(
    model: Gpt3Model,
    prompt: str | None = None,
    max_tokens: int | None = None,
    temperature: float | None = None
) -> dict:
    """
        Text Completion
        https://platform.openai.com/docs/api-reference/completions/create
    """
    data = {'model': model}
    if prompt is not None:
        data['prompt'] = prompt
    
    if max_tokens is not None:
        data['max_tokens'] = max_tokens
    
    if temperature is not None:
        data['temperature'] = temperature

    resp = await client.post(
        url="/v1/completions",
        json=data,
        timeout=10
    )

    if resp.is_server_error:
        resp.raise_for_status()

    if resp.is_client_error:
        raise OpenAiException.from_resp(resp)

    return resp.json()


async def create_chat_completion(
    model: Literal['gpt-3.5-turbo', 'gpt-3.5-turbo-0301'],
    messages: list[Message],
    temperature: float | None = None
):
    """
        Chat Completion (ChatGPT)
        https://platform.openai.com/docs/api-reference/chat/create
    """
    data = {
        'model': model,
        'messages': messages
    }

    if temperature is not None:
        data['temperature'] = temperature

    resp = await client.post(
        url='/v1/chat/completions',
        json=data,
        timeout=20
    )

    if resp.is_server_error:
        resp.raise_for_status()

    if resp.is_client_error:
        raise OpenAiException.from_resp(resp)

    return resp.json()


async def create_image(
    prompt: str,
    n: int | None = None,
    size: ImageSize | None = None
):
    """
        Image Generation.
        https://platform.openai.com/docs/api-reference/images/create
    """
    data = {'prompt': prompt}
    if n is not None:
        data['n'] = n
    
    if size is not None:
        data['size'] = size

    resp = await client.post(
        url="/v1/images/generations",
        json=data
    )

    if resp.is_server_error:
        resp.raise_for_status()

    if resp.is_client_error:
        raise OpenAiException.from_resp(resp)

    return resp.json()


async def moderations(
    input: str,
    model: Literal['text-moderation-stable', 'text-moderation-latest'] | None = None
):
    """
        Moderations
        https://platform.openai.com/docs/api-reference/moderations/create
    """
    data = {'input': input}
    if model is not None:
        data['model'] = model

    resp = await client.post(
        url="/v1/moderations",
        json=data
    )

    if resp.is_server_error:
        resp.raise_for_status()

    if resp.is_client_error:
        raise OpenAiException.from_resp(resp)

    return resp.json()
