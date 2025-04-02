import logging
from telegram import Update, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, ContextTypes

from bot.functions import start, mainmenu_callback, start_quiz, handle_quiz_answer
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

def main():
    application = ApplicationBuilder().token(BotConfig.telegram_token).build()

    # back_handler = RegexHandler(pattern='^(' + Keyboards.back + ')$', callback=show_categories, pass_user_data=True)
    start_handler = MessageHandler(filters.TEXT & filters.Regex("^/start$"), callback=start)
    button_handler = CallbackQueryHandler(button_handler_callback, pattern='[b_]\w*')

    # Quiz conversation handler
    quiz_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_quiz, pattern="^start_quiz$")],
        states={
            QUIZ_STATES["QUIZ_QUESTION_1"]: [CallbackQueryHandler(handle_quiz_answer, pattern="^quiz_answer_")],
            QUIZ_STATES["QUIZ_QUESTION_2"]: [CallbackQueryHandler(handle_quiz_answer, pattern="^quiz_answer_")],
            QUIZ_STATES["QUIZ_QUESTION_3"]: [CallbackQueryHandler(handle_quiz_answer, pattern="^quiz_answer_")],
        },
        fallbacks=[]
    )

    # Add handlers
    application.add_handler(start_handler)
    application.add_handler(quiz_conv_handler)
    application.add_handler(CallbackQueryHandler(mainmenu_callback, pattern="^(main_menu)$"))
    
    # Run the bot
    application.run_polling(poll_interval=5)


async def button_handler_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == 'b_entry':
        reply_keyboard = [[KeyboardButton(text="ارسال موقعیت", request_location=True)]]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await context.bot.sendMessage(query.message.chat_id, query.data, reply_markup=reply_markup)
    else:
        await query.message.reply_text(query.data, reply_markup=ReplyKeyboardRemove())
