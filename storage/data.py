from pydantic import BaseModel


class Data(BaseModel):
    data: dict[str, list[int]]
