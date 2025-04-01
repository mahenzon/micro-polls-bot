from aiogram import types

from storage.data import Data
from utils.compression import decode_data
from utils.consts import URL_FOR_DATA
from utils.url_data import extract_data_url


def extract_data(message: types.Message) -> Data:
    data_url = extract_data_url(message.entities)
    return decode_data(data_url.removeprefix(URL_FOR_DATA))
