from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.types import (
    InputTextMessageContent,
    InlineQueryResultArticle,
)
from aiogram.utils import markdown

from utils.polls import prepare_poll_parameters_data, prepare_send_poll_keyboard

router = Router(name="inline")


@router.inline_query()
async def inline_query_handler(inline_query: types.InlineQuery) -> None:
    poll_params = prepare_poll_parameters_data(inline_query.query)

    keyboard = prepare_send_poll_keyboard(
        poll_params.question_text,
        poll_params.answers,
    )
    prepared_message_text = markdown.text(
        markdown.hbold("Press the button to send the question message"),
        markdown.html_decoration.quote(poll_params.question_text),
        sep="\n\n",
    )
    input_content = InputTextMessageContent(
        message_text=prepared_message_text,
        parse_mode=ParseMode.HTML,
    )

    result_item = InlineQueryResultArticle(
        id=inline_query.id,  # something unique
        title=poll_params.title,
        description=poll_params.description,
        input_message_content=input_content,
        reply_markup=keyboard,
    )
    results = [result_item]
    await inline_query.answer(results)
