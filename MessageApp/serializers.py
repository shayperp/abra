from rest_framework import serializers
from MessageApp.models import Users, Messages


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'name')


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ('id', 'sender', 'recipient', 'message', 'subject', 'timestamp', 'is_read')
