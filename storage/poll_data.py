from pydantic import BaseModel


class PollData(BaseModel):
    data: dict[str, set[int]]
