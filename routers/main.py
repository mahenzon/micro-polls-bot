__all__ = ("router",)

from aiogram import Router

from .echo import router as echo_router

router = Router(name="main")
router.include_routers(
    echo_router,
)
