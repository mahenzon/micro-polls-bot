from aiogram.types import MessageEntity

from utils.consts import URL_FOR_DATA


def extract_data_url(entities: list[MessageEntity]) -> str | None:
    for entity in entities:
        if entity.url and entity.url.startswith(URL_FOR_DATA):
            return entity.url

    return None
