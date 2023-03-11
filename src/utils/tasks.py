import asyncio
import uuid

from models import OpenAiChatMessage
from services.openai import create_text_completion, create_chat_completion,\
    create_image, Gpt3Model, Gpt35Model, ImageSize
from services.telnyx import send_message
from utils.encryption import f


# ~~~ Background Tasks ~~~

async def create_image_and_send_message(prompt: str, from_: str, to: str):
    result = await create_image(
        prompt=prompt,
        size=ImageSize.SMALL
    )
    url = result['data'][0]['url']
    await send_message(from_=from_, to=to, text="", media_urls=[url])


async def create_text_completion_and_send_message(prompt: str, from_: str, to: str):
    result = await create_text_completion(
        model=Gpt3Model.CURIE,
        prompt=prompt,
        max_tokens=128
    )
    text = result['choices'][0]['text']
    await send_message(from_=from_, to=to, text=text)


async def create_chat_completion_and_send_message(
    message_content: str,
    user_uuid: uuid.UUID,
    from_: str,
    to: str
):
    # Add new message.
    user_message = OpenAiChatMessage.new(
        user_uuid=user_uuid,
        role='user',
        content=message_content
    )
    await user_message.insert()

    # Query for previous messages.
    cursor = OpenAiChatMessage.find(
        query={
            'user_uuid': user_uuid,
        },
        limit=20
    )

    messages = [
        {'role': msg.role, 'content': msg.content}
        async for msg in cursor
    ]
    
    result = await create_chat_completion(
        model=Gpt35Model.TURBO,
        messages=messages
    )

    assistant_message = OpenAiChatMessage.new(
        user_uuid=user_uuid,
        role=result['choices'][0]['message']['role'],
        content=result['choices'][0]['message']['content']
    )

    await asyncio.gather(
        assistant_message.insert(),
        send_message(from_=from_, to=to, text=assistant_message.content)
    )
