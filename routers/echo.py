__all__ = ("router",)

from aiogram import Router
from aiogram.types import Message

router = Router(name="echo")


@router.message()
async def message_handler(message: Message) -> None:
    await message.answer(message.text)
