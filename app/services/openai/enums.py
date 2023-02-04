from enum import StrEnum


class Gpt3Model(StrEnum):
    DAVINCI = 'text-davinci-003'
    CURIE = 'text-curie-001'
    BABBAGE = 'text-babbage-001'
    ADA = 'text-ada-001'


class ImageSize(StrEnum):
    SMALL = '256x256'
    MEDIUM = '512x512'
    LARGE = '1024x1024'
