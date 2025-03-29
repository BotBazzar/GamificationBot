import json
import logging

import persian
from telegram import (ReplyKeyboardMarkup, LabeledPrice, SuccessfulPayment, Update, InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import *

from constants.employee_constants import BotMessages, ConversationStates

from db.db_handler import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

logger = logging.getLogger()
FULL_NAME, EMP_ID, DONE = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(start.__name__)
    chat_id = update.message.chat_id
    if user_exists(chat_id):
        kb = [InlineKeyboardButton("منو اصلی", callback_data="main_menu")]
        reply_keyboard = [kb]
        reply_markup = InlineKeyboardMarkup(reply_keyboard)
        await update.message.reply_text(BotMessages.help, reply_markup=reply_markup)
        return ConversationHandler.END

    print("user_exict")
    kb = [InlineKeyboardButton("ثبت نام", callback_data="register")]
    reply_keyboard = [kb]
    reply_markup = InlineKeyboardMarkup(reply_keyboard)
    await update.message.reply_text(BotMessages.register, reply_markup=reply_markup)
    return FULL_NAME


async def mainmenu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # extract the callback query and chat id from the update object
    buttons = [{'text': "انگشت‌زنی مجازی", 'callback_data': "b_entry"},
               {'text': "کار خارج از اداره", 'callback_data': "b_out_work"},
               {'text': "ثبت مرخصی", 'callback_data': "b_leave"},
               {'text': "ثبت\اصلاح کار", 'callback_data': "b_work_report"},
               {'text': "تنظیمات", 'callback_data': "b_settings"}, {'text': "راهنما", 'callback_data': "b_help"}]
    if user_is_leader(update.callback_query.message.chat_id):
        buttons.insert(4, {'text': "گزارش‌گیری", 'callback_data': "b_records"})
    reply_keyboard = [[InlineKeyboardButton(text=b['text'], callback_data=b['callback_data'])] for b in buttons]
    reply_markup = InlineKeyboardMarkup(reply_keyboard)

    query = update.callback_query
    print("query: --->", query)
    chat_id = query.message.chat_id

    await context.bot.sendMessage(chat_id, BotMessages.choose_from_buttons, reply_markup=reply_markup)


async def register_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # extract the callback query and chat id from the update object
    query = update.callback_query
    chat_id = query.message.chat_id

    await context.bot.sendMessage(chat_id, BotMessages.full_name)
    return EMP_ID


async def received_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(received_name.__name__)
    # extract the callback query and chat id from the update object
    firstname = update.message.text
    context.user_data['full_name'] = firstname
    await update.message.reply_text(BotMessages.employee_id)
    return DONE


async def received_employee_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(received_employee_id.__name__)
    # extract the callback query and chat id from the update object
    emp_id = update.message.text
    context.user_data['employee_id'] = emp_id

    add_new_user(context.user_data['full_name'], update.message.chat_id, emp_id)

    kb = [InlineKeyboardButton("منو اصلی", callback_data="main_menu")]
    reply_keyboard = [kb]
    reply_markup = InlineKeyboardMarkup(reply_keyboard)

    await update.message.reply_text(BotMessages.register_success)
    await update.message.reply_text(BotMessages.help, reply_markup=reply_markup)
    return ConversationHandler.END


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_pos = (update.message.location.latitude, update.message.location.longitude)
    print(update.message)
    print(current_pos)
    await update.message.reply_text("موقعیت مکانی شما دریافت شد.")
