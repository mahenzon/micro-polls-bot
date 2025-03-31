__all__ = ("router",)

from aiogram import Router

from .inline import router as inline_router
from .echo import router as echo_router

router = Router(name="main")
router.include_routers(
    inline_router,
    echo_router,
)
