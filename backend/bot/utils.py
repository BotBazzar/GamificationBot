import os
from telegram import Bot

from main_config import BotConfig

async def set_webhook():
    bot = Bot(token=BotConfig.telegram_token)
    webhook_url = f"{BotConfig.webhook_domain}{BotConfig.webhook_path}"
    await bot.set_webhook(webhook_url)