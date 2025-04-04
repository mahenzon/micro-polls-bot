from typing import Any

from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.utils import markdown
from utils.consts import MAX_ANSWER_SIZE
from utils.polls import prepare_poll_parameters_data

router = Router(name="commands")


@router.message(CommandStart())
async def handle_command_start(message: types.Message):
    return message.answer("Send /poll")


@router.message(Command("help", prefix="!/"))
async def handle_command_help(message: types.Message):
    return message.answer("Send /poll to create poll. Any questions? @SurenTalk")


@router.message(Command("poll", prefix="!/"))
async def poll_command(
    message: types.Message,
    command: CommandObject,
) -> Any:
    poll_params = prepare_poll_parameters_data(command.args)
    if poll_params.example:
        example_command = (
            f"{command.prefix}{command.command} {poll_params.as_question_string}"
        )
        prepared_message_text = markdown.text(
            markdown.hbold(poll_params.question_text),
            markdown.hcode(markdown.html_decoration.quote(example_command)),
            sep="\n\n",
        )
        return message.reply(
            text=prepared_message_text,
            parse_mode=ParseMode.HTML,
        )

    if not poll_params.question_text:
        return message.reply(text="No question text found. Try better.")
    if len(poll_params.answers) != len(set(poll_params.answers)):
        return message.reply(text="Options have to be unique.")
    if any(len(answer) > MAX_ANSWER_SIZE for answer in poll_params.answers):
        return message.reply(text="Some answers are too long. Make them shorter.")
    text, keyboard = poll_params.build()
    return message.reply(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )
