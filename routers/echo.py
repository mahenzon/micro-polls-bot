__all__ = ("router",)

from typing import Any

from aiogram import F, Router
from aiogram.types import Message, ReactionTypeEmoji

router = Router(name="echo")


@router.message(F.text)
async def message_handler(message: Message) -> Any:
    if message.chat.type == "private":
        return message.answer(message.text)
    return message.react([ReactionTypeEmoji(emoji="👍")])
