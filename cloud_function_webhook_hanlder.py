import base64
import io
import logging
from typing import Any

from aiogram import Bot
from aiogram.methods import TelegramMethod
from aiogram.methods.base import TelegramType
from aiogram.types import Update
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import JsonPayload, Payload

log = logging.getLogger(__name__)


class AsyncBytesIO:
    def __init__(self):
        self.buffer = io.BytesIO()

    async def write(self, data):
        # Simulate asynchronous writing
        return self.buffer.write(data)

    def getvalue(self):
        return self.buffer.getvalue()


async def write_body_to_string(writer: Payload):
    async_buffer = AsyncBytesIO()

    # noinspection PyTypeChecker
    await writer.write(async_buffer)

    base64_encoded = base64.b64encode(async_buffer.getvalue()).decode("utf-8")

    return base64_encoded


class CloudFunctionWebhookHandler(SimpleRequestHandler):
    DEFAULT_STATUS_CODE = 200

    def _build_response_writer(
        self,
        bot: Bot,
        result: TelegramMethod[TelegramType] | None,
    ) -> Payload:
        """
        # we need to return something "empty"
        # and "empty" form doesn't work
        # since it's sending only "end" boundary w/o "start"
        https://github.com/aiogram/aiogram/pull/1665
        """
        if not result:
            return JsonPayload({})

        return super()._build_response_writer(bot, result)

    async def handle_raw_event(self, json_body: str) -> TelegramMethod[Any] | None:
        try:
            return await self.dispatcher.feed_webhook_update(
                self.bot,
                Update.model_validate_json(json_body),
                **self.data,
            )
        except Exception as e:
            log.exception("Could not handle webhook event %s", e)

    async def handle_yandex_cloud_function(self, event: dict) -> dict[str, str]:
        result: TelegramMethod[Any] | None = await self.handle_raw_event(
            json_body=event["body"],
        )
        response_writer = self._build_response_writer(bot=self.bot, result=result)
        body_as_base64_string: str = await write_body_to_string(response_writer)
        return {
            "statusCode": self.DEFAULT_STATUS_CODE,
            "headers": dict(response_writer.headers.items()),
            "multiValueHeaders": {},
            "body": body_as_base64_string,
            "isBase64Encoded": True,
        }
