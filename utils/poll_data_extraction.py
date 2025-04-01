from aiogram import types
from aiogram.types import MessageEntity
from storage.poll_data import PollData

from utils.compression import decode_data
from utils.consts import URL_FOR_DATA


def extract_data_url(entities: list[MessageEntity]) -> str | None:
    for entity in entities:
        if entity.url and entity.url.startswith(URL_FOR_DATA):
            return entity.url

    return None


def extract_poll_data(message: types.Message) -> PollData:
    data_url = extract_data_url(message.entities)
    return decode_data(data_url.removeprefix(URL_FOR_DATA))


def extract_question_from_message_text(message_text: str) -> str:
    return message_text.strip().split(
        "\n",
        maxsplit=1,
    )[0]
