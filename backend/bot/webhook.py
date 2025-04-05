from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, PollAnswerHandler
from telegram import Update, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup

from .functions import (
    start,
    mainmenu_callback,
    start_quiz,
    receive_quiz_answer,
)
from main_config import BotConfig

async def webhook(request):
    application = ApplicationBuilder().token(BotConfig.telegram_token).build()

    # Add conversation handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(mainmenu_callback, pattern="^main_menu$"))
    application.add_handler(CallbackQueryHandler(start_quiz, pattern="^start_quiz$"))
    application.add_handler(PollAnswerHandler(receive_quiz_answer))

    
    # Process webhook request
    update = await application.bot.get_updates()
    await application.process_update(update)
    
    return "OK"