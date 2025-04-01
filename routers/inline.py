from typing import Any

from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.types import (
    InputTextMessageContent,
    InlineQueryResultArticle,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils import markdown

from utils.compression import compress_string
from utils.url_data import QUESTION_SEP

router = Router(name="inline")


def prepare_data(input_query: str) -> tuple[Any, ...]:

    if input_query and QUESTION_SEP in input_query:
        question_text, *answers = input_query.split(QUESTION_SEP)
        title = question_text
        description = f"Answers: {f' {QUESTION_SEP} '.join(answers)}"
    else:
        question_text = "Yes or No?"
        answers = ["Yes", "No"]
        example_question_string = QUESTION_SEP.join([question_text, *answers])
        title = "Example question"
        description = f"Ask your question:\n{example_question_string}"

    return (
        title,
        description,
        question_text,
        answers,
    )


def prepare_keyboard(
    question_text: str,
    answers: list,
) -> InlineKeyboardMarkup:
    question_data_string = QUESTION_SEP.join([question_text, *answers])
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Press me!",
                    callback_data=compress_string(question_data_string),
                ),
            ],
        ],
    )


@router.inline_query()
async def inline_query_handler(inline_query: types.InlineQuery) -> None:
    (
        title,
        description,
        question_text,
        answers,
    ) = prepare_data(inline_query.query)

    keyboard = prepare_keyboard(question_text, answers)
    prepared_message_text = markdown.text(
        markdown.hbold("Press the button to send the question message"),
        markdown.html_decoration.quote(question_text),
        sep="\n\n",
    )
    input_content = InputTextMessageContent(
        message_text=prepared_message_text,
        parse_mode=ParseMode.HTML,
    )

    result_item = InlineQueryResultArticle(
        id=inline_query.id,  # something unique
        title=title,
        description=description,
        input_message_content=input_content,
        reply_markup=keyboard,
    )
    results = [result_item]
    await inline_query.answer(results)
