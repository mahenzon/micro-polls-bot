import asyncio

from bot import create_bot
from cloud_function_webhook_hanlder import CloudFunctionWebhookHandler
from dispatcher import create_dispatcher

dp = create_dispatcher()
bot = create_bot()
webhook_requests_handler = CloudFunctionWebhookHandler(
    dispatcher=dp,
    bot=bot,
    handle_in_background=False,
)


def handle(event, context):
    return asyncio.get_event_loop().run_until_complete(
        webhook_requests_handler.handle_yandex_cloud_function(
            event=event,
        ),
    )
