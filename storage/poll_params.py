from pydantic import BaseModel, ConfigDict

from utils.consts import QUESTION_SEP


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
