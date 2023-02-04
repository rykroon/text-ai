from services.openai import create_completion, create_image, Gpt3Model, ImageSize
from services.telnyx import send_message


# ~~~ Background Tasks ~~~

async def create_image_and_send_message(prompt: str, from_: str, to: str):
    result = await create_image(
        prompt=prompt,
        size=ImageSize.SMALL
    )
    url = result['data'][0]['url']
    await send_message(from_=from_, to=to, text="", media_urls=[url])


async def create_completion_and_send_message(prompt: str, from_: str, to: str):
    result = await create_completion(
        model=Gpt3Model.CURIE,
        prompt=prompt,
        max_tokens=64
    )
    text = result['choices'][0]['text']
    await send_message(from_=from_, to=to, text=text)
