import logging

from telegram import (Update, InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import *

from constants.messages import BotMessages
from constants.quiz import QuizConstants
from db.db_handler import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

logger = logging.getLogger()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(start.__name__)
    chat_id = update.message.chat_id
    user = update.message.from_user
    print(user)
    if not user_exists(chat_id):
        add_new_user(chat_id,user.username,user.first_name,user.last_name)

    welcome_message = BotMessages.welcome
    if user.first_name:
        welcome_message = f" سلام {user.first_name} عزیز،\n\n{welcome_message}"

    kb = [InlineKeyboardButton("منو اصلی", callback_data="main_menu")]
    reply_keyboard = [kb]
    reply_markup = InlineKeyboardMarkup(reply_keyboard)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


async def mainmenu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        {'text': "🎮 بازی‌های سرگرم‌کننده", 'callback_data': "b_games"},
        {'text': "🏆 رتبه‌بندی", 'callback_data': "b_leaderboard"},
        {'text': "🎁 جوایز", 'callback_data': "b_rewards"},
        {'text': "🎯 چالش‌ها", 'callback_data': "b_challenges"},
        {'text': "📚 راهنمای بازاریابی گیمیفیکیشن", 'callback_data': "b_guide"},
        {'text': "کوییز", 'callback_data': "start_quiz"}
    ]

    reply_keyboard = [[InlineKeyboardButton(text=b['text'], callback_data=b['callback_data'])] for b in buttons]
    reply_markup = InlineKeyboardMarkup(reply_keyboard)

    query = update.callback_query
    await query.edit_message_text(BotMessages.menu, reply_markup=reply_markup)


async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the quiz"""
    if not user_exists(update.message.chat_id):
        await update.message.reply_text(BotMessages.not_registered)
        return ConversationHandler.END

    context.user_data['quiz'] = {
        'correct': 0,
        'incorrect': 0,
        'current_question': 0
    }

    await update.message.reply_text(QuizConstants.messages['start'])

    # Start first question
    question = QuizConstants.questions[0]
    options = question['options']

    reply_keyboard = [[InlineKeyboardButton(text=opt, callback_data=f"quiz_answer_{opt}")] for opt in options]
    reply_markup = InlineKeyboardMarkup(reply_keyboard)

    await update.message.reply_text(
        QuizConstants.messages['question'].format(number=1, question=question['question']),
        reply_markup=reply_markup
    )

    return QuizConstants.states['QUIZ_QUESTION_1']


async def handle_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle quiz answers"""
    query = update.callback_query
    answer = query.data.split('_')[-1]
    current_question = context.user_data['quiz']['current_question']

    # Get current question
    question = QuizConstants.questions[current_question]

    # Check if answer is correct
    if answer == question['correct']:
        context.user_data['quiz']['correct'] += 1
        response = QuizConstants.messages['correct'].format(explanation=question['explanation'])
    else:
        context.user_data['quiz']['incorrect'] += 1
        response = QuizConstants.messages['incorrect'].format(
            correct=question['correct'],
            explanation=question['explanation']
        )

    await query.answer()
    await query.edit_message_text(response)

    # Move to next question
    current_question += 1

    if current_question < len(QuizConstants.questions):
        # Show next question
        next_question = QuizConstants.questions[current_question]
        options = next_question['options']

        reply_keyboard = [[InlineKeyboardButton(text=opt, callback_data=f"quiz_answer_{opt}")] for opt in options]
        reply_markup = InlineKeyboardMarkup(reply_keyboard)

        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=QuizConstants.messages['question'].format(number=current_question + 1,
                                                           question=next_question['question']),
            reply_markup=reply_markup
        )

        context.user_data['quiz']['current_question'] = current_question
        return QuizConstants.states[f'QUIZ_QUESTION_{current_question + 1}']
    else:
        # Quiz completed
        correct = context.user_data['quiz']['correct']
        incorrect = context.user_data['quiz']['incorrect']

        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=QuizConstants.messages['completed'].format(
                correct=correct,
                incorrect=incorrect
            )
        )

        # Save quiz results to database
        await save_quiz_results(query.message.chat_id, correct, incorrect)

        return ConversationHandler.END


async def save_quiz_results(chat_id: int, correct: int, incorrect: int):
    """Save quiz results to database"""
    try:
        user = User.objects.get(chat_id=chat_id)
        result = QuizResult(user=user, correct=correct, incorrect=incorrect)
        result.save()
    except Exception as e:
        logger.error(f"Error saving quiz results: {str(e)}")
