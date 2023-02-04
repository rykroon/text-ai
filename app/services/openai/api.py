import os
import httpx

from .enums import Gpt3Model, ImageSize
from .exceptions import OpenAiException


API_KEY = os.environ['OPENAI_API_KEY']


client = httpx.AsyncClient(
    base_url="https://api.openai.com",
    headers={'Authorization': f"Bearer {API_KEY}"},
    http2=True
)


async def create_completion(model: Gpt3Model, prompt: str, max_tokens: int = 16) -> dict:
    resp = await client.post(
        url="/v1/completions",
        json={
            'model': model,
            'prompt': prompt,
            'max_tokens': max_tokens
        },
        timeout=10
    )

    if resp.is_server_error:
        resp.raise_for_status()
    
    if resp.is_client_error:
        raise OpenAiException.from_resp(resp)

    return resp.json()


async def create_image(prompt: str, size: ImageSize):
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
