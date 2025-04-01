from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import markdown
from pydantic import BaseModel, ConfigDict

from storage.data import Data
from utils.compression import compress_data
from utils.consts import QUESTION_SEP, URL_FOR_DATA


def prepare_poll_data(
    question: str,
    answers: list[str],
    existing_data: Data | None = None,
) -> tuple[str, InlineKeyboardMarkup]:
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
    data = existing_data or Data(data={})
    compressed_data = compress_data(data)
    link_with_data = f"{URL_FOR_DATA}{compressed_data}"
    message_text = markdown.text(
        markdown.hide_link(link_with_data),
        markdown.html_decoration.quote(question),
    )
    return message_text, answers_kb


class PollParams(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    title: str
    description: str
    question_text: str
    answers: list[str]
    example: bool

    @property
    def as_question_string(self) -> str:
        return f" {QUESTION_SEP} ".join([self.question_text, *self.answers])

    def build(
        self,
        existing_data: Data | None = None,
    ) -> tuple[str, InlineKeyboardMarkup]:
        return prepare_poll_data(
            question=self.question_text,
            answers=self.answers,
            existing_data=existing_data,
        )
