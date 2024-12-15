from aiogram import Router
from .all_commands.cmd_adminPanel import router as admin_router
from .all_commands.cmd_started import router as sign_up_router
from .all_commands.cmd_help import router as help_func_router
from .all_f_text.personal_information_handler import router as personal_information_router
from .all_f_text.operating_system_handler import router as operating_system_router
from .all_f_text.technical_support_handler import router as technical_support_handler
from .all_f_text.connected_handler import router as connected_router
from .all_f_text.back_data_handler import router as back_router

router = Router()

router.include_router(admin_router)
router.include_router(sign_up_router)
router.include_router(help_func_router)
router.include_router(personal_information_router)
router.include_router(operating_system_router)
router.include_router(technical_support_handler)
router.include_router(connected_router)
router.include_router(back_router)