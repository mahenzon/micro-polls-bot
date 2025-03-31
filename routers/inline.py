from aiogram import Router, types
from aiogram.types import (
    InputTextMessageContent,
    InlineQueryResultArticle,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

router = Router(name="inline")


@router.inline_query()
async def inline_query_handler(inline_query: types.InlineQuery) -> None:
    title = "Example question"
    description = "Ask your question:\nQuestion | Yes | No"
    text = "Yes or No?"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Yes",
                    callback_data="yes",
                ),
                InlineKeyboardButton(
                    text="No",
                    callback_data="no",
                ),
            ],
        ],
    )
    input_content = InputTextMessageContent(
        message_text=text,
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
