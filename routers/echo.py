__all__ = ("router",)

from aiogram import F, Router
from aiogram.types import Message, ReactionTypeEmoji

router = Router(name="echo")


@router.message(F.text)
async def message_handler(message: Message) -> None:
    if message.chat.type == "private":
        await message.answer(message.text)
        return
    await message.react([ReactionTypeEmoji(emoji="👍")])
