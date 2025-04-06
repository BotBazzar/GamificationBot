import asyncio

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .webhook import get_application
from telegram import Update


class WebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        update = request.data
        try:
            process_bot_update(get_application, update)
        except Exception as e:
            print(e)
        finally:
            print('finally error or not')

        return Response({}, status=200)


def process_bot_update(bot_main, update):
    async def connectToBot():
        app = bot_main()
        async with app:
            await app.start()
            await app.update_queue.put(Update.de_json(data=update, bot=app.bot))
            await app.stop()

    asyncio.run(connectToBot())
