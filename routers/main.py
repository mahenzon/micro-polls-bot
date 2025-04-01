__all__ = ("router",)

from aiogram import Router

from .buttons import router as buttons_router
from .commands import router as commands_router
from .echo import router as echo_router
from .inline import router as inline_router

router = Router(name="main")
router.include_routers(
    inline_router,
    buttons_router,
    commands_router,
    echo_router,
)
