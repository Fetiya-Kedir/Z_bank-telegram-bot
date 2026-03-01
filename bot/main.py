from __future__ import annotations

import logging

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from bot.config import load_settings
from bot.handlers.commands import language_command
from bot.handlers.fallback import unknown_callback, unknown_text
from bot.handlers.language import language_callback
from bot.handlers.menu import menu_callback
from bot.handlers.nav import nav_callback
from bot.handlers.start import start_command
from bot.utils.logger import setup_logging

logger = logging.getLogger(__name__)


def build_app() -> Application:
    settings = load_settings()
    setup_logging(settings.log_level)

    app = Application.builder().token(settings.telegram_bot_token).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("language", language_command))

    # Callbacks (specific patterns first)
    app.add_handler(CallbackQueryHandler(language_callback, pattern=r"^lang:"))
    app.add_handler(CallbackQueryHandler(menu_callback, pattern=r"^menu:"))
    app.add_handler(CallbackQueryHandler(nav_callback, pattern=r"^nav:"))

    # Callback fallback (must be LAST among callbacks)
    app.add_handler(CallbackQueryHandler(unknown_callback))

    # Text fallback (non-command text)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_text))

    return app


def main() -> None:
    app = build_app()
    logger.info("Starting bot...")
    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()