from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import Message, FriendRequest

from django.db.models import Q

class FriendsFilter(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        request = self.context['request']
        friends = FriendRequest.objects.filter(Q(askTo=request.user) & Q(approved=True))

        list_friend = []
        for friend in friends:
            list_friend.append(friend.askFrom.id)

        queryset = get_user_model().objects.filter(id__in=list_friend)
        return queryset

class MessageSerializer(serializers.ModelSerializer):

    receiver = FriendsFilter()

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'message')
        extra_kwargs = {'sender': {'read_only': True}}