from __future__ import annotations

import logging

from telegram.ext import Application, CallbackQueryHandler, CommandHandler

from bot.config import load_settings
from bot.handlers.language import language_callback
from bot.handlers.menu import menu_callback
from bot.handlers.start import start_command
from bot.utils.logger import setup_logging

logger = logging.getLogger(__name__)


def build_app() -> Application:
    settings = load_settings()
    setup_logging(settings.log_level)

    app = Application.builder().token(settings.telegram_bot_token).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))

    # Callbacks
    app.add_handler(CallbackQueryHandler(language_callback, pattern=r"^lang:"))
    app.add_handler(CallbackQueryHandler(menu_callback, pattern=r"^menu:"))

    return app


def main() -> None:
    app = build_app()
    logger.info("Starting bot...")
    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()