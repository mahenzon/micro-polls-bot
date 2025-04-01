from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject
from aiogram.utils import markdown

from utils.polls import prepare_poll_parameters_data

router = Router(name="commands")


@router.message(Command("poll", prefix="!/"))
async def poll_command(
    message: types.Message,
    command: CommandObject,
) -> None:
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
        await message.reply(
            text=prepared_message_text,
            parse_mode=ParseMode.HTML,
        )
        return None

    await message.reply(
        text=markdown.text(
            poll_params.question_text,
            poll_params.description,
            sep="\n",
        )
    )
