from rest_framework import serializers
from accounts.models import CustomUser
from .models import Room

class PairStudentsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    # Include other user fields as needed
    room_id = serializers.IntegerField(source='id')
    room_interest = serializers.CharField()
    # Include other room fields as needed
