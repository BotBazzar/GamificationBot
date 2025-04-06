import json
import logging

from telegram import (Update, InlineKeyboardButton,
                      InlineKeyboardMarkup, Poll, WebAppInfo)
from telegram.ext import *

from constants.messages import BotMessages
from constants.quiz import QuizConstants
from db.db_handler import *

# Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
#
logger = logging.getLogger()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(start.__name__)
    chat_id = update.message.chat_id
    user = update.message.from_user
    is_user=await user_exists(chat_id)
    if not is_user:
        await add_new_user(chat_id, user.username, user.first_name, user.last_name)

    welcome_message = BotMessages.welcome
    if user.first_name:
        welcome_message = f" سلام {user.first_name} عزیز،\n\n{welcome_message}"

    kb = [InlineKeyboardButton("منو اصلی", callback_data="main_menu")]
    reply_keyboard = [kb]
    reply_markup = InlineKeyboardMarkup(reply_keyboard)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


async def mainmenu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    b_leaderboard = [InlineKeyboardButton('🏆 رتبه‌بندی', web_app=WebAppInfo(url='https://erfanfaravani.ir/#/leaderboard'))]
    b_rewards = [InlineKeyboardButton('🎁 جوایز', callback_data="b_rewards")]
    b_challenges = [InlineKeyboardButton('🎯 چالش‌ها', callback_data="start_quiz")]
    reply_keyboard = [b_leaderboard, b_rewards, b_challenges]
    reply_markup = InlineKeyboardMarkup(reply_keyboard)

    query = update.callback_query
    await query.edit_message_text(BotMessages.menu, reply_markup=reply_markup)


async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the quiz by sending all questions at once"""
    query = update.callback_query
    
    chat_id = query.message.chat_id
    user = query.message.from_user
    
    if not await user_exists(chat_id):
        await add_new_user(chat_id, user.username, user.first_name, user.last_name)

    await query.message.reply_text(QuizConstants.messages.get('start', None))
    await query.answer()

    # Send all questions
    for question in QuizConstants.questions:
        options = question['options']
        correct_option = options.index(question['correct'])

        # Send the poll
        message = await context.bot.send_poll(
            chat_id=chat_id,
            question=question['question'],
            options=options,
            type=Poll.QUIZ,
            correct_option_id=correct_option,
            is_anonymous=False,
            explanation=question['explanation']
        )
        
        # Store poll info with poll_id
        context.bot_data[message.poll.id] = {
            "question": question['question'],
            "chat_id": chat_id,
            "correct_option": correct_option,
            "explanation": question['explanation']
        }

        b_wheel = [
            InlineKeyboardButton('گردونه شانس 🎰', web_app=WebAppInfo(url='https://erfanfaravani.ir/#/'))]
        reply_keyboard = [b_wheel]
        reply_markup = InlineKeyboardMarkup(reply_keyboard)
    await context.bot.send_message(chat_id,"هم اکنون می‌توانید گردانه شانس را بچرخانید",reply_markup=reply_markup)


async def receive_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle quiz answers and update user scores"""
    poll_answer = update.poll_answer
    user = poll_answer.user
    chat_id = user.id
    
    # Get the question that was answered using poll_id
    poll_data = context.bot_data.get(str(poll_answer.poll_id))
    if not poll_data:
        return

    question = poll_data['question']
    correct_option = poll_data['correct_option']
    
    # Update user's score
    if poll_answer.option_ids[0] == correct_option:
        await update_user_score(chat_id, 1)  # Add 1 point for correct answer
    else:
        await update_user_score(chat_id, 0)  # No points for incorrect answer
