__all__ = ("router",)

from aiogram import F, Router
from aiogram.types import Message

router = Router(name="echo")


@router.message(F.text)
async def message_handler(message: Message) -> None:
    await message.answer(message.text)
