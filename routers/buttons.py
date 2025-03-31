import base64

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router(name="buttons")


def decode_and_decompress(encoded_data: str) -> str:
    """
    Decode the Base64 data
    TODO: Decompress the data using zlib
    """
    string_data = base64.urlsafe_b64decode(encoded_data)

    return string_data.decode()


@router.callback_query(F.inline_message_id)
async def handle_callback_send_message(query: CallbackQuery) -> None:
    question_data = decode_and_decompress(query.data)
    await query.answer("Cool!")

    question, *answers = question_data.split("|")
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
    await query.bot.send_message(
        chat_id=query.from_user.id,
        text=question.strip(),
        reply_markup=answers_kb,
    )


@router.callback_query(F.message.text)
async def handle_callback_message_has_text(query: CallbackQuery) -> None:
    if not (query.message and query.message.text):
        await query.answer("No message text found.")
        return

    message_text = query.message.text
    entities = query.message.entities
    print("message text:", message_text)
    print("entities:", entities)
    print("cb data:", query.data)
    await query.answer()
