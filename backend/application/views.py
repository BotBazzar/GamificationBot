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