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
    print(user)
    if not user_exists(chat_id):
        add_new_user(chat_id, user.username, user.first_name, user.last_name)

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
    """Start the quiz"""
    query = update.callback_query
    
    chat_id = query.message.chat_id
    user = query.message.from_user
    
    if not user_exists(chat_id):
        add_new_user(chat_id, user.username, user.first_name, user.last_name)

    context.user_data['quiz'] = {
        'correct': 0,
        'incorrect': 0,
        'current_question': 0
    }

    await query.message.reply_text(QuizConstants.messages.get('start', None))
    await query.answer()

    # Start first question
    question = QuizConstants.questions[0]
    options = question['options']
    correct_option = options.index(question['correct'])

    # Save quiz data in context
    payload = {
        question['question']: {
            "chat_id": chat_id,
            "message_id": None,
            "correct_option": correct_option,
            "explanation": question['explanation']
        }
    }
    context.bot_data.update(payload)
    # Send the quiz
    message = await context.bot.send_poll(
        chat_id=chat_id,
        question=question['question'],
        options=options,
        type=Poll.QUIZ,
        correct_option_id=correct_option,
        is_anonymous=False,  # 🔥 This is important!
        explanation=question['explanation']
    )
    
    # Update message_id in payload
    payload[question['question']]['message_id'] = message.message_id
    context.bot_data.update(payload)

    return QuizConstants.states.get('QUIZ_QUESTION_1')


async def receive_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle quiz answers"""
    poll_answer = update.poll_answer
    user = poll_answer.user
    chat_id = user.id
    await context.bot.send_message(chat_id, f"User {user.first_name} {user.last_name} answered: {poll_answer.option_ids[0]}")
    try:
        quiz_data = context.bot_data[poll_answer.poll_id]
    except KeyError:
        return

    # Check if this is the correct question
    if quiz_data['message_id'] != context.bot_data[poll.question]['message_id']:
        return
    await update.effective_message.reply_text("QuizConstants.messages.get('quiz_answer', None)")
    # Get current question
    current_question = context.user_data['quiz']['current_question']
    # Check if answer is correct
    if poll_answer.option_ids[0] == quiz_data['correct_option']:
        context.user_data['quiz']['correct'] += 1
    else:
        context.user_data['quiz']['incorrect'] += 1

    # Move to next question
    current_question += 1

    if current_question < len(QuizConstants.questions):
        # Show next question
        next_question = QuizConstants.questions[current_question]
        options = next_question['options']
        correct_option = options.index(next_question['correct'])

        # Save new quiz data
        payload = {
            next_question['question']: {
                "chat_id": quiz_data['chat_id'],
                "message_id": None,
                "correct_option": correct_option,
                "explanation": next_question['explanation']
            }
        }
        context.bot_data.update(payload)

        # Send next question
        message = await context.bot.send_poll(
            chat_id=quiz_data['chat_id'],
            question=next_question['question'],
            options=options,
            type=Poll.QUIZ,
            correct_option_id=correct_option,
            explanation=next_question['explanation']
        )

        # Update message_id in payload
        payload[next_question['question']]['message_id'] = message.message_id
        context.bot_data.update(payload)

        context.user_data['quiz']['current_question'] = current_question
        return QuizConstants.states[f'QUIZ_QUESTION_{current_question + 1}']
    else:
        # Quiz completed
        correct = context.user_data['quiz']['correct']
        incorrect = context.user_data['quiz']['incorrect']
        
        await context.bot.send_message(
            chat_id=quiz_data['chat_id'],
            text=QuizConstants.messages['completed'].format(
                correct=correct,
                incorrect=incorrect
            )
        )
        
        # Save quiz results to database
        await save_quiz_results(quiz_data['chat_id'], correct, incorrect)

        return QuizConstants.states['QUIZ_COMPLETED']


async def save_quiz_results(chat_id: int, correct: int, incorrect: int):
    """Save quiz results to database"""
    try:
        user = User.objects.get(chat_id=chat_id)
        result = QuizResult(user=user, correct=correct, incorrect=incorrect)
        result.save()
    except Exception as e:
        logger.error(f"Error saving quiz results: {str(e)}")


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a predefined poll"""
    questions = ["1", "2", "4", "20"]
    message = await update.effective_message.reply_poll(
        "How many eggs do you need for a cake?", questions, type=Poll.QUIZ, correct_option_id=2
    )
    # Save some info about the poll the bot_data for later use in receive_quiz_answer
    payload = {
        message.poll.id: {"chat_id": update.effective_chat.id, "message_id": message.message_id}
    }
    context.bot_data.update(payload)


# async def receive_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Close quiz after three participants took it"""
#     # the bot can receive closed poll updates we don't care about
#     if update.poll.is_closed:
#         return
#     if update.poll.total_voter_count == TOTAL_VOTER_COUNT:
#         try:
#             quiz_data = context.bot_data[update.poll.id]
#         # this means this poll answer update is from an old poll, we can't stop it then
#         except KeyError:
#             return
#         await context.bot.stop_poll(quiz_data["chat_id"], quiz_data["message_id"])
