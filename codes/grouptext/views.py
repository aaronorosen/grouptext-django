from django.http import HttpResponse
from django.conf import settings
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
import json

import logging

from .serializers import TextGroupSerializer, TextGroupMemberSerializer
from .serializers import TextQuestionSerializer, TextMessageSerializer
from .models import TextGroup, TextGroupMember, TextQuestion, TextMessage
from .twilio import send_confirmation_code, twilio_send_sms
# Create your views here.


def index(request):
    return HttpResponse("Hello World")


class TextGroupViewSet(viewsets.ModelViewSet):
    queryset = TextGroup.objects.all().order_by('group_name')
    serializer_class = TextGroupSerializer


class TextGroupMemberViewSet(viewsets.ModelViewSet):
    queryset = TextGroupMember.objects.all().order_by('text_group')
    serializer_class = TextGroupMemberSerializer


class TextQuestionViewSet(viewsets.ModelViewSet):
    queryset = TextQuestion.objects.all().order_by('text_group')
    serializer_class = TextQuestionSerializer


class TextMessageViewSet(viewsets.ModelViewSet):
    queryset = TextMessage.objects.all().order_by('dest_phone')
    serializer_class = TextMessageSerializer


@api_view(['POST'])
def add_group_member(request, group_id):

    # look up textgroup from textgroup_id
    text_group = TextGroup.objects.get(id=group_id)

    text_group_member = TextGroupMember()
    text_group_member.member_name = request.data.get("member_name")
    text_group_member.member_phone = request.data.get("member_phone")
    text_group_member.text_group = text_group
    text_group_member.save()

    return Response({'id': text_group_member.id})


@api_view(['POST'])
def ask_group_question(request, group_id):

    # look up textgroup from textgroup_id
    text_group = TextGroup.objects.get(id=group_id)

    text_question = TextQuestion()
    text_question.text_group = text_group
    text_question.question = request.data.get("question")
    text_question.save()

    return Response({'id': text_question.id})

@api_view(['POST'])
@parser_classes([JSONParser])
def send_sms(request):
    # Here we get the key that holds the phone number and the message
    send_message_detail = request.data['messaging_content']
    logging.warning(send_message_detail)

    sms_response = twilio_send_sms(send_message_detail['message_number'], send_message_detail['message_content'])
    logging.warning(sms_response)

    # DONE: Insert the details into the db
    text_message = TextMessage()
    text_message.message = send_message_detail['message_content']
    text_message.dest_phone = send_message_detail['message_number']
    text_message.src_phone = settings.TWILIO['TWILIO_NUMBER']
    text_message.message_id = sms_response['message_id']
    text_message.message_status = sms_response['status']
    text_message.save()

    # This should have the the mobile number and the message in it as json form
    # Response({"Status": message.delivery.status, "message": "Your message has/n't been sent"})
    return Response({"Phone_number": send_message_detail['message_number'],
                     "message": send_message_detail['message_content'],
                     "message_status": sms_response['status']})



@api_view(['POST'])
def sms_final_status(request):
    # TODO: Get the response from the status callback by twilio and then from there
    #  get the message id match with the message id in db (already there cos of initial sending of message)
    #  then update the status in the table to [delivered, undelivered] etc.

    logging.warning(request)
    return Response({"response": "No content", "status": 204})

@api_view(['GET'])
def get_groups_and_members(request):

    text_groups_members = []
    text_groups = TextGroup.objects.all()
    for text_group in text_groups:
        text_group_info = {
            'group_id': text_group.id,
            'group_name': text_group.group_name,
            'members': [],
            'questions': [],
        }

        text_questions = TextQuestion.objects.filter(
            text_group=text_group).all()

        for text_question in text_questions:
            text_group_info['questions'].append({
                'question': text_question.question,
                'sent': text_question.sent,
                'text_question_id': text_question.id,
            })

        text_group_members = TextGroupMember.objects.filter(
            text_group=text_group).all()

        for text_group_member in text_group_members:
            text_group_info['members'].append({
                'member_name': text_group_member.member_name,
                'member_phone': text_group_member.member_phone,
                'member_id': text_group_member.id,
            })

        text_groups_members.append(text_group_info)

    return Response(text_groups_members)
