from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import (
    CallbackQuery,
)

from utils.compression import (
    decode_and_decompress,
    decode_data,
)
from utils.poll_params import prepare_poll_data
from utils.url_data import extract_data_url
from utils.consts import URL_FOR_DATA, QUESTION_SEP

router = Router(name="buttons")


@router.callback_query(F.inline_message_id)
async def handle_callback_send_message(query: CallbackQuery) -> None:
    await query.answer("Cool!")
    question_data = decode_and_decompress(query.data)
    question, *answers = question_data.split(QUESTION_SEP)
    question, answers_kb = prepare_poll_data(
        question=question,
        answers=answers,
    )
    await query.bot.send_message(
        chat_id=query.from_user.id,
        text=question,
        reply_markup=answers_kb,
        parse_mode=ParseMode.HTML,
    )


@router.callback_query(F.message.text)
async def handle_callback_message_has_text(query: CallbackQuery) -> None:
    data_url = extract_data_url(query.message.entities)
    message_text = query.message.text
    print("message id:", query.message.message_id)
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
