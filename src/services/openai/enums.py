from enum import StrEnum


# https://openai.com/pricing


class Gpt35Model(StrEnum):
    """
    https://platform.openai.com/docs/models/gpt-3-5

    GPT-3.5 models can understand and generate natural language or code.
    Our most capable and cost effective model is gpt-3.5-turbo which is
    optimized for chat but works well for traditional completions tasks as well.
    """

    TURBO = "gpt-3.5-turbo"
    TURBO_0301 = "gpt-3.5-turbo-0301"
    TEXT_DAVINCI_3 = "text-davinci-003"
    TEXT_DAVINCI_2 = "text-davinci-002"
    CODE_DAVINCI_2 = "code-davinci-002"


class Gpt3Model(StrEnum):
    """
    https://platform.openai.com/docs/models/gpt-3

    GPT-3 models can understand and generate natural language.
    These models were superceded by the more powerful GPT-3.5 generation models.
    However, the original GPT-3 base models (davinci, curie, ada, and babbage)
    are currently the only models that are available to fine-tune.
    """

    TEXT_CURIE = "text-curie-001"
    TEXT_BABBAGE = "text-babbage-001"
    TEXT_ADA = "text-ada-001"
    DAVINCI = "davinci"
    CURIE = "curie"
    BABBAGE = "babbage"
    ADA = "ada"


class CodexModel(StrEnum):
    """
    https://platform.openai.com/docs/models/codex

    The Codex models are descendants of our GPT-3 models that can
    understand and generate code. Their training data contains both
    natural language and billions of lines of public code from GitHub.
    They’re most capable in Python and proficient in over a dozen
    languages including JavaScript, Go, Perl, PHP, Ruby, Swift,
    TypeScript, SQL, and even Shell.
    """

    DAVINCI = "code-davinci-002"
    CUSHMAN = "code-cushman-001"


class ImageSize(StrEnum):
    SMALL = "256x256"
    MEDIUM = "512x512"
    LARGE = "1024x1024"
