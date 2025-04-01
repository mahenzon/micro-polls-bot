__all__ = ("create_dispatcher",)

from aiogram import Dispatcher
from routers.main import router as main_router


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher(name="dispatcher")
    dispatcher.include_router(router=main_router)

    return dispatcher
