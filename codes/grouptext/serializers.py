from rest_framework import serializers
from .models import TextGroup, TextGroupMember, TextQuestion, TextMessage


class TextGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TextGroup
        fields = ('id', 'group_name', 'created_at')


class TextGroupMemberSerializer(serializers.HyperlinkedModelSerializer):
    textgroup = TextGroupSerializer(read_only=True)

    class Meta:
        model = TextGroupMember
        fields = '__all__'


class TextQuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TextQuestion
        fields = ('id', 'text_group', 'question', 'created_at')


class TextMessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TextMessage
        fields = ('message', 'dest_phone', 'src_phone', 'created_at')


