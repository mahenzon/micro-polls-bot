from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import (
    CallbackQuery,
)

from storage.data import Data
from utils.compression import (
    decode_and_decompress,
)
from utils.poll_data_extractor import extract_data
from utils.poll_params import prepare_poll_data
from utils.consts import QUESTION_SEP

router = Router(name="buttons")


@router.callback_query(F.inline_message_id)
async def handle_callback_send_message(query: CallbackQuery) -> None:
    await query.answer("Cool!")
    question_data = decode_and_decompress(query.data)
    question, *answers = question_data.split(QUESTION_SEP)
    message_text, answers_kb = prepare_poll_data(
        question=question,
        answers=answers,
    )
    await query.bot.send_message(
        chat_id=query.from_user.id,
        text=message_text,
        reply_markup=answers_kb,
        parse_mode=ParseMode.HTML,
    )


@router.callback_query(
    F.message.text,
    F.message.entities,
    F.message.func(extract_data).as_("extracted_data"),
)
async def handle_callback_message_has_text_end_entity(
    query: CallbackQuery,
    extracted_data: Data,
) -> None:
    message_text = query.message.text
    print("message id:", query.message.message_id)
    print("message text:", message_text)
    print("cb data:", query.data)
    print("entities:", query.message.entities)

    print("data.data:", extracted_data.data)
    await query.answer("Works!")


@router.callback_query(
    F.message.text,
    F.message.entities,
    F.func(extract_data).as_("extracted_data"),
)
async def handle_callback_invalid(
    query: CallbackQuery,
) -> None:
    await query.answer("No data available")
