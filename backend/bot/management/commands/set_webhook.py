from django.core.management.base import BaseCommand
from bot.utils import set_webhook

class Command(BaseCommand):
    help = 'Set up Telegram bot webhook'

    async def handle(self, *args, **options):
        await set_webhook()
        self.stdout.write(self.style.SUCCESS('Webhook set up successfully'))