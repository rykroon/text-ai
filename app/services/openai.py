from enum import StrEnum
import os
import httpx


API_KEY = os.environ['OPENAI_API_KEY']


client = httpx.AsyncClient(
    base_url="https://api.openai.com",
    headers={'Authorization': f"Bearer {API_KEY}"},
    http2=True
)


class Gpt3Model(StrEnum):
    DAVINCI = 'text-davinci-003'
    CURIE = 'text-curie-001'
    BABBAGE = 'text-babbage-001'
    ADA = 'text-ada-001'


class ImageSize(StrEnum):
    SMALL = '256x256'
    MEDIUM = '512x512'
    LARGE = '1024x1024' 


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
    resp.raise_for_status()
    return resp.json()


async def create_image(prompt: str, size: ImageSize):
    resp = await client.post(
        url="/v1/images/generations",
        json={
            'prompt': prompt,
            'size': size
        }
    )
    resp.raise_for_status()
    return resp.json()
