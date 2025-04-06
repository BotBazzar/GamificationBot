from django.shortcuts import render

from application.serializers import UserSerializer
from db.models import User
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class GetUsersInfoView(APIView):
    def get(self, request):
        users = User.objects.all()  # Get all users
        serializer = UserSerializer(users, many=True)  # Serialize users
        return Response(serializer.data)  # Return serialized data


class GetLeaderboardView(APIView):
    def get(self, request):
        users =  User.objects.all().order_by('-score')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=200)


class GetPrizesView(APIView):
    def get(self, request):
        chat_id = request.query_params.get('chat_id')
        if not chat_id:
            return Response({"error": "chat_id is required"}, status=400)
        user = User.objects.get(chat_id=chat_id)
        return Response({
            "prizeIndex": user.prize,
            "hasSpun": user.has_spun,
            "prizeList": [
                {"name": "کارت بازی"},
                {"name": "گل یا پوچ"},
                {"name": "مارپله"},
                {"name":"پوچ"},
                {"name": "کارت بازی"},
                {"name": "گل یا پوچ"},
                {"name": "مارپله"},
            ]
        })

    def post(self, request):
        chat_id= request.query_params.get('chat_id')
        if not chat_id:
            return Response({"error": "chat_id is required"}, status=400)
        user = User.objects.get(chat_id=chat_id)
        user.has_spun = True
        user.save()
        return Response({"message": "Prize marked as spun"})
