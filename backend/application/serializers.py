from rest_framework import serializers
from db.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['chat_id', 'username', 'first_name', 'last_name', 'score', 'answers', 'has_spun', 'prize', 'create_at']



