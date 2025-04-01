from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import markdown

from storage.data import Data
from storage.poll_params import PollParams
from utils.compression import compress_string, compress_data
from utils.consts import QUESTION_SEP, URL_FOR_DATA


def prepare_poll_parameters_data(input_query: str) -> PollParams:

    if input_query and QUESTION_SEP in input_query:
        question_text, *answers = input_query.split(QUESTION_SEP)
        title = question_text
        description = f"Answers: {f' {QUESTION_SEP} '.join(answers)}"
        example = False
    else:
        question_text = "Yes or No?"
        answers = ["Yes", "No"]
        example_question_string = QUESTION_SEP.join([question_text, *answers])
        title = "Example question"
        description = f"Ask your question:\n{example_question_string}"
        example = True

    return PollParams(
        title=title,
        description=description,
        question_text=question_text,
        answers=answers,
        example=example,
    )


def prepare_send_poll_keyboard(
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


def prepare_poll_data(
    question_data: str,
) -> tuple[str, InlineKeyboardMarkup]:

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
    return question, answers_kb
