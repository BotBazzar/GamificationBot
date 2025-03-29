import logging

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, ApplicationBuilder, \
    CallbackQueryHandler, ConversationHandler, MessageHandler, filters, ContextTypes

from bot.functions import start, register_callback, received_name, received_employee_id, mainmenu_callback, location
from main_config import BotConfig

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

START, END = range(2)
FULL_NAME, EMP_ID, DONE = range(3)


def main():
    application = ApplicationBuilder().token(BotConfig.telegram_token).build()
    # application = ApplicationBuilder().token(BotConfig.tousradiehhr_token).base_url(
    #     BotConfig.base_url).base_file_url(BotConfig.base_file_url).build()

    # back_handler = RegexHandler(pattern='^(' + Keyboards.back + ')$', callback=show_categories, pass_user_data=True)
    start_handler = MessageHandler(filters.TEXT & filters.Regex("^/start$"), callback=start)
    button_handler = CallbackQueryHandler(button_handler_callback, pattern='[b_]\w*')
    location_handler = MessageHandler(filters.LOCATION, location)
    register_conv_handler = ConversationHandler(entry_points=[start_handler],
                                                states={
                                                    FULL_NAME: [
                                                        CallbackQueryHandler(register_callback, pattern="^register$")],
                                                    EMP_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                                                            received_name,
                                                                            )],
                                                    DONE: [MessageHandler(
                                                        filters.TEXT & ~filters.COMMAND,
                                                        received_employee_id,
                                                    )],
                                                }, fallbacks=[])

    application.add_handler(
        CallbackQueryHandler(mainmenu_callback, pattern="^(main_menu)$")
    )
    application.add_handler(button_handler)
    application.add_handler(location_handler)
    application.add_handler(register_conv_handler)

    application.run_polling(poll_interval=3)


async def button_handler_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == 'b_entry':
        reply_keyboard = [[KeyboardButton(text="ارسال موقعیت", request_location=True)]]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await context.bot.sendMessage(query.message.chat_id, query.data, reply_markup=reply_markup)
    else:
        await query.message.reply_text(query.data, reply_markup=ReplyKeyboardRemove())
