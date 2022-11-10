import json
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from api.models import Message, Room
from api.serializers import MessageSerializer


def get_users(members):
    users = set()
    for member in members:
        if(member):
            user = User.objects.get(id=member)
            users.add(user)
    print(f"users: {users}")
    return users


def get_room(request, room_name):
    if not Room.objects.filter(room_name=room_name).exists():
        room = Room.objects.create(room_name=room_name, owner=request.user)
    else:
        room = Room.objects.get(room_name=room_name)

    return room


def main_view(request, room_name='common'):
    if not request.user.is_authenticated:
        return redirect('index')

    room = get_room(request, room_name)
    room.members.set(User.objects.all())
    rooms = Room.objects.filter(room_name=room_name)
    messages = Message.objects.filter(room__room_name=room_name)
    if request.method == "GET":

        return render(request, 'chat/chat.html',
                      {'users': User.objects.all(),
                       'messages': messages,
                       'room_name': room_name,
                       'room': room,
                       'rooms': rooms,
                       })


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if request.method == 'GET':
        messages = Message.objects.filter(
            sender_id=sender, is_read=False)
        serializer = MessageSerializer(
            messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def room_view(request):
    print()
    print('room_view')
    print()
    all_users = User.objects.all()
    if request.method == "POST":
        data = json.loads(request.body)
        room_name = data.get("room_name")
        members = data.get("members")
        print(f'members: {members}')
        room = get_room(request, room_name)
        users = get_users(members)
        users.add(room.owner)
        room.members.set(users)
        room.save()

        return render(request, "chat/chat.html",
                      {
                          'users': users,
                          'room': room,
                          'room_name': room_name,
                      })
    return render(request, 'chat/room.html', {
        'users': all_users,
    })


@csrf_exempt
def chat_view(request, room_name):
    print()
    print('chat_view')
    print()
    if not request.user.is_authenticated:
        return redirect('index')
    print(f'room_name: {room_name}')

    rooms = Room.objects.all()
    room = get_room(request, room_name)

    messages = Message.objects.filter(room__room_name=room_name)
    if(room_name == 'common'):
        users = User.objects.all()
    else:
        users = Room.objects.get(room_name=room_name).members.all()

    return render(request, "chat/chat.html",
                  {
                      'users': users,
                      'rooms': rooms,
                      'room': room,
                      'messages': messages,
                      'room_name': room_name,
                  })
