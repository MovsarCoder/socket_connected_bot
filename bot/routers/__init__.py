from aiogram import Router

from bot.routers.commands.admin_panel import router as admin_router
from bot.routers.commands.help import router as help_func_router
from bot.routers.commands.start import router as sign_up_router
from bot.routers.text.back import router as back_router
from bot.routers.text.connected import router as connected_router
from bot.routers.text.operating_system import router as operating_system_router
from bot.routers.text.personal_information import router as personal_information_router
from bot.routers.text.technical_support import router as technical_support_handler

router = Router()

router.include_router(admin_router)
router.include_router(sign_up_router)
router.include_router(help_func_router)
router.include_router(personal_information_router)
router.include_router(operating_system_router)
router.include_router(technical_support_handler)
router.include_router(connected_router)
router.include_router(back_router)
