from rest_framework import serializers
from db.models import User, QuizResult

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['chat_id', 'username', 'first_name', 'last_name', 'create_at']

class QuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResult
        fields = ['id', 'user', 'correct', 'incorrect']

