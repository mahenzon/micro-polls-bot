from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.poll_params import PollParams
from utils.compression import compress_string
from utils.consts import QUESTION_SEP


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
