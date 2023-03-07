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
    return await client.get('v1/models')
 

async def create_text_completion(
    model: Gpt3Model,
    prompt: str,
    max_tokens: int = 16,
    temperature: float = 1.0
) -> dict:
    """
        Text Completion
    """
    resp = await client.post(
        url="/v1/completions",
        json={
            'model': model,
            'prompt': prompt,
            'max_tokens': max_tokens,
            'temperature': temperature
        },
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
):
    """
        Chat Completion (ChatGPT)
    """
    resp = await client.post(
        url='/v1/chat/completions',
        json={
            'model': model,
            'messages': messages
        },
        timeout=20
    )

    if resp.is_server_error:
        resp.raise_for_status()

    if resp.is_client_error:
        raise OpenAiException.from_resp(resp)

    return resp.json()


async def create_image(prompt: str, size: ImageSize):
    """
        Image Generation.
    """
    resp = await client.post(
        url="/v1/images/generations",
        json={
            'prompt': prompt,
            'size': size
        }
    )

    if resp.is_server_error:
        resp.raise_for_status()

    if resp.is_client_error:
        raise OpenAiException.from_resp(resp)

    return resp.json()


async def moderations(input: str):
    """
        Moderations
    """
    resp = await client.post(
        url="/v1/moderations",
        json={
            'input': input
        }
    )

    if resp.is_server_error:
        resp.raise_for_status()

    if resp.is_client_error:
        raise OpenAiException.from_resp(resp)

    return resp.json()
