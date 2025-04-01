from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    MessageEntity,
)
from aiogram.utils import markdown

from storage.data import Data
from utils.compression import (
    decode_and_decompress,
    compress_data,
    decode_data,
)
from utils.url_data import URL_FOR_DATA, QUESTION_SEP

router = Router(name="buttons")


@router.callback_query(F.inline_message_id)
async def handle_callback_send_message(query: CallbackQuery) -> None:
    question_data = decode_and_decompress(query.data)
    await query.answer("Cool!")

    question, *answers = question_data.split(QUESTION_SEP)
    answers_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=answer.strip(),
                    callback_data=answer.strip(),
                )
                for answer in answers
            ]
        ]
    )
    data = Data(
        data={
            "foo": [1, 2, 3],
            "bar": [4, 5, 6],
        },
    )
    compressed_data = compress_data(data)
    link_with_data = f"{URL_FOR_DATA}{compressed_data}"
    question = markdown.text(
        markdown.hide_link(link_with_data),
        markdown.html_decoration.quote(question),
    )
    await query.bot.send_message(
        chat_id=query.from_user.id,
        text=question,
        reply_markup=answers_kb,
        parse_mode=ParseMode.HTML,
    )


def extract_data_url(entities: list[MessageEntity]) -> str | None:
    for entity in entities:
        if entity.url and entity.url.startswith(URL_FOR_DATA):
            return entity.url

    return None


@router.callback_query(F.message.text)
async def handle_callback_message_has_text(query: CallbackQuery) -> None:
    data_url = extract_data_url(query.message.entities)
    message_text = query.message.text
    print("message text:", message_text)
    print("cb data:", query.data)
    print("entities:", query.message.entities)

    if not data_url:
        await query.answer("No data available")
        return
    data = decode_data(data_url.removeprefix(URL_FOR_DATA))
    print("data url:", data_url)
    print("data.data:", data.data)
    await query.answer()
