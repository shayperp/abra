from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.db.models import Q
from MessageApp.models import Messages
from MessageApp.serializers import MessagesSerializer


@csrf_exempt
def add_message(request):
    message_data = JSONParser().parse(request)
    message_serializer = MessagesSerializer(data=message_data)
    is_valid = message_serializer.is_valid()
    if is_valid:
        message_serializer.save()
        return JsonResponse("Added message successfully", safe=False)
    return JsonResponse("Failed to add message", safe=False)


@csrf_exempt
def get_messages(request, user_id):
    messages = Messages.objects.filter(Q(sender=user_id) | Q(recipient=user_id))
    messages_serializer = MessagesSerializer(messages, many=True)
    return JsonResponse(messages_serializer.data, safe=False)


@csrf_exempt
def get_unread_messages(request, user_id):
    messages = Messages.objects.filter(is_read__in=[False]).filter(Q(sender=user_id) | Q(recipient=user_id))
    messages_serializer = MessagesSerializer(messages, many=True)
    return JsonResponse(messages_serializer.data, safe=False)


@csrf_exempt
def read_message(request, message_id):
    message = Messages.objects.get(id=message_id)
    message.is_read = True
    message.save()
    message_serializer = MessagesSerializer(message)
    return JsonResponse(message_serializer.data, safe=False)


@csrf_exempt
def delete_message(request, message_id, user_id):
    message = Messages.objects.get(id=message_id)
    if user_id in (message.sender.id, message.recipient.id):
        message.delete()
        return JsonResponse('Successfully deleted', safe=False)
    return JsonResponse('Failed to delete message', safe=False)
