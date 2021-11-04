from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.db.models import Q
from MessageApp.models import Messages
from MessageApp.serializers import MessagesSerializer
from django.contrib.auth import authenticate, login, logout


@csrf_exempt
def homepage(request):
    return render(request, 'readme.html')


@csrf_exempt
def login_app(request):
    request_data = JSONParser().parse(request)
    user = authenticate(request, username=request_data.get('username'), password=request_data.get('password'))
    if user is not None:
        login(request, user)
        return JsonResponse("Login success", safe=False)
    else:
        return JsonResponse("Failed to login", safe=False)


@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse("Logged out", safe=False)


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
def get_messages(request):
    if request.user.is_authenticated:
        messages = Messages.objects.filter(Q(sender=request.user.id) | Q(recipient=request.user.id))
        messages_serializer = MessagesSerializer(messages, many=True)
        return JsonResponse(messages_serializer.data, safe=False)
    else:
        return JsonResponse("Failed to get messages, need to log in first", safe=False)


@csrf_exempt
def get_unread_messages(request):
    if request.user.is_authenticated:
        messages = Messages.objects.filter(is_read__in=[False]).filter(Q(sender=request.user.id) | Q(recipient=request.user.id))
        messages_serializer = MessagesSerializer(messages, many=True)
        return JsonResponse(messages_serializer.data, safe=False)
    else:
        return JsonResponse("Failed to get unread messages, need to log in first", safe=False)


@csrf_exempt
def read_message(request, message_id):
    try:
        message = Messages.objects.get(id=message_id)
    except Exception:
        return JsonResponse('Failed to read message, message id not exist', safe=False)
    message.is_read = True
    message.save()
    message_serializer = MessagesSerializer(message)
    return JsonResponse(message_serializer.data, safe=False)


@csrf_exempt
def delete_message(request, message_id):
    if request.user.is_authenticated:
        try:
            message = Messages.objects.get(id=message_id)
        except Exception:
            return JsonResponse('Failed to delete message, message id not exist', safe=False)
        if request.user.id in (message.sender.id, message.recipient.id):
            message.delete()
            return JsonResponse('Successfully deleted', safe=False)
        return JsonResponse('Failed to delete message, this user cant delete this message', safe=False)
    return JsonResponse("Failed to get delete message, need to log in first", safe=False)
