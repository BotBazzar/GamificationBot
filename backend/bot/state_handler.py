import logging
from telegram import Update, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, \
    filters, ContextTypes, PollHandler, PollAnswerHandler

from bot.functions import start, mainmenu_callback, start_quiz, receive_quiz_answer
from main_config import BotConfig
from constants.quiz import QuizConstants

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

# States
START, END = range(2)
FULL_NAME, EMP_ID, DONE = range(3)

# Quiz states
QUIZ_STATES = {
    "QUIZ_START": "quiz_start",
    "QUIZ_QUESTION_1": "quiz_question_1",
    "QUIZ_QUESTION_2": "quiz_question_2",
    "QUIZ_QUESTION_3": "quiz_question_3",
    "QUIZ_COMPLETED": "quiz_completed"
}

def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(BotConfig.telegram_token).build()

    # Add conversation handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(mainmenu_callback, pattern="^main_menu$"))
    application.add_handler(CallbackQueryHandler(start_quiz, pattern="^start_quiz$"))
    application.add_handler(PollAnswerHandler(receive_quiz_answer))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES,poll_interval=5)


async def button_handler_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == 'b_entry':
        reply_keyboard = [[KeyboardButton(text="ارسال موقعیت", request_location=True)]]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await context.bot.sendMessage(query.message.chat_id, query.data, reply_markup=reply_markup)
    else:
        await query.message.reply_text(query.data, reply_markup=ReplyKeyboardRemove())
