import base64

from aiogram import Router, types
from aiogram.types import (
    InputTextMessageContent,
    InlineQueryResultArticle,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

router = Router(name="inline")


def compress_string(text: str) -> str:
    """
    TODO: compress using zlib
    base64 encode
    """
    encoded_data = base64.urlsafe_b64encode(text.encode())
    return encoded_data.decode()


@router.inline_query()
async def inline_query_handler(inline_query: types.InlineQuery) -> None:
    validated_string = inline_query.query or "Yes or No? | Yes | No"

    title = "Example question"
    description = f"Ask your question:\n{validated_string}"
    question_text, _ = validated_string.split("|", maxsplit=1)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Press me!",
                    callback_data=compress_string(validated_string),
                ),
            ],
        ],
    )
    input_content = InputTextMessageContent(
        message_text=question_text,
    )

    result_item = InlineQueryResultArticle(
        id=inline_query.id,  # something unique
        title=title,
        description=description,
        input_message_content=input_content,
        reply_markup=keyboard,
    )
    results = [result_item]
    await inline_query.answer(results)
