from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import markdown
from pydantic import BaseModel, ConfigDict

from storage.poll_data import PollData
from utils.compression import compress_data
from utils.consts import (
    QUESTION_SEP,
    URL_FOR_DATA,
)


def prepare_message_text_with_data_link(
    question_text: str,
    poll_data: PollData,
) -> str:
    compressed_data = compress_data(poll_data)

    text_link_with_data = markdown.hide_link(f"{URL_FOR_DATA}{compressed_data}")
    answers_with_counts = markdown.text(
        *(
            markdown.text("-", f"{markdown.hbold(answer)}:", len(pros))
            for answer, pros in poll_data.data.items()
        ),
        sep="\n",
    )
    return markdown.text(
        text_link_with_data,
        markdown.text(
            markdown.html_decoration.quote(question_text),
            "",
            answers_with_counts,
            sep="\n",
        ),
        sep="",
    )


def prepare_poll_data(
    question: str,
    answers: list[str],
    poll_data: PollData | None = None,
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
    message_text = prepare_message_text_with_data_link(
        question_text=question,
        poll_data=poll_data or PollData(data={}),
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
        poll_data: PollData | None = None,
    ) -> tuple[str, InlineKeyboardMarkup]:
        return prepare_poll_data(
            question=self.question_text,
            answers=self.answers,
            poll_data=poll_data,
        )
