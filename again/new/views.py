from django.shortcuts import render, redirect
from .models import User, Room, Message
from django.http import HttpResponse, JsonResponse
# Create your views here.
def index(request):
    return render(request, 'index.html')
def checkview(request):
 
        room_name = request.POST.get('room_name')
        username = request.POST.get('username')
        if Room.objects.filter(name= room_name).exists():
            return redirect('/'+room_name+'/?username='+username)
        else:
            new_room = Room.objects.create(name=room_name)
            new_room.save()
            return redirect('/'+room_name+'/?username='+username)
    
def sign(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')   
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
            return render(request, 'sign.html', {'error': 'Email already exists.'})
        
        
        else:
            User.objects.create(name=name, email=email, password=password)  
            return render(request, 'login.html' )  
    
    return render(request, 'sign.html')
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        if User.objects.filter(email=email, password=password).exists():
            return render(request, 'index.html', )
        else:
            
            return render(request, 'login.html', {'error': 'Invalid email or password.'})
    return render(request, 'login.html')

def room(request, room_name):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room_name)
    return render(request, 'room.html', {
        'username': username,
        'room': room_name,
        'room_details': room_details
    })
def find(request):
    
    return render(request, 'find.html')
def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room_name):
    room_details = Room.objects.get(name=room_name)
    messages = Message.objects.filter(room=room_details.id)

    # convert datetimes to strings (important, otherwise JSON serialization fails)
    message_list = []
    for msg in messages:
        message_list.append({
            'user': msg.user,
            'value': msg.value,
            'date': msg.date.strftime('%Y-%m-%d %H:%M:%S') if msg.date else ''
        })

    return JsonResponse({'messages': message_list})

    