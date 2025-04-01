from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import (
    CallbackQuery,
)
from storage.poll_data import PollData
from utils.compression import (
    decode_and_decompress,
)
from utils.consts import QUESTION_SEP
from utils.poll_data_extraction import (
    extract_poll_data,
    extract_question_from_message_text,
)
from utils.poll_params import prepare_message_text_with_data_link, prepare_poll_data
from utils.polls import RESULTS_MAP, handle_vote

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
    F.message.func(extract_poll_data).as_("poll_data"),
)
async def handle_callback_message_has_text_end_entity(
    query: CallbackQuery,
    poll_data: PollData,
) -> None:
    result = handle_vote(
        poll_data=poll_data,
        user_id=query.from_user.id,
        response=query.data.strip(),
    )
    await query.answer(RESULTS_MAP[result])

    question_text = extract_question_from_message_text(query.message.text)
    message_text = prepare_message_text_with_data_link(
        question_text=question_text,
        poll_data=poll_data,
    )
    await query.message.edit_text(
        text=message_text,
        reply_markup=query.message.reply_markup,
        parse_mode=ParseMode.HTML,
    )


@router.callback_query(
    F.message.text,
    F.message.entities,
    F.func(extract_poll_data).as_("extracted_data"),
)
async def handle_callback_invalid(
    query: CallbackQuery,
) -> None:
    await query.answer("No data available")
