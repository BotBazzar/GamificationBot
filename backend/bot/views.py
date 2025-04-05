from django.http import JsonResponse
from .webhook import webhook

async def telegram_webhook(request):
    if request.method == 'POST':
        await webhook(request)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)