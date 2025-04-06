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
        return Response({"message": "Hello, Leaderboard!"})


class GetPrizesView(APIView):
    def get(self, request):
        return Response({
            "prizeIndex": 3,
            "hasSpun": True,
            "imageUrl": "https://example.com/images/prize3.png",
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
        return Response({"message": "Hello, Prizes!"})
