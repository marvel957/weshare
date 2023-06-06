from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic,Message
from .forms import create_room_form,UserForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q 
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, "username does not exist")

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "login successful")
            return redirect('home')
        else:
            messages.error(request, "username or password is invalid") 
    context ={'page':page}
    return render(request,'base/login_register.html',context)
def registerPage(request):
    form = UserCreationForm
    page = 'register'
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')
    context ={'page':page,'form':form} 
    return render(request,'base/login_register.html',context)
def logoutPage(request):
    logout(request)     
    return redirect('login')

def UserProfile(request,pk):
    user = User.objects.get(id = pk)
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    rooms = user.room_set.all()

    context = {'user':user,'rooms':rooms,'topics':topics,'room_messages':room_messages}
    return render(request,'base/userprofile.html',context)
def home(request):
    q = request.GET.get('q') if request.GET.get('q')  != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q)| Q(description__icontains = q)|Q(name__icontains = q)|Q(host__username__icontains = q))
    room_count = rooms.count()
    topics = Topic.objects.all()[0:3]
    room_messages = Message.objects.filter(room__topic__name__icontains = q).order_by('-created','-updated')

    context = {'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/index.html',context)
def room(request,pk):
    room = Room.objects.get(pk = pk)
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST['body']
        )
        room.participants.add(request.user)
        return redirect('room',pk = room.id)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    context = {'room':room,'room_messages':room_messages,'participants':participants}
    return render(request, 'base/room.html',context)
@login_required(login_url='login')
def CreateRoom(request):
    if request.method == 'POST':
        topic,created = Topic.objects.get_or_create(name = request.POST['topic'])
        Room.objects.create(
            host = request.user,
            topic = topic,
            name  = request.POST['room_name'],
            description = request.POST['room_description']
        )
        return redirect('home')
    topics = Topic.objects.all()
    form =  create_room_form()
    context = {'form':form,'topics':topics}
    return render(request, 'base/create-room.html',context)
@login_required(login_url='login')
def UpdateRoom(request,pk):
    topics = Topic.objects.all()
    room = Room.objects.get(pk = pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed here")
    if request.method == 'POST':
        topic,created = Topic.objects.get_or_create(name = request.POST['topic'])
        room.topic = topic
        room.name =  request.POST['room_name']
        room.description =  request.POST['room_description']
        room.save()
        return redirect('home')
    form =  create_room_form(instance = room)
    context = {'form':form,'topics':topics,'room':room}
    return render(request, 'base/create-room.html',context)
@login_required(login_url='login')
def DeleteRoom(request,pk):
    room = Room.objects.get(pk = pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed here")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj':room}
    return render(request, 'base/deleteroom.html',context)
@login_required(login_url='login')
def DeleteMessage(request,pk):
    message = Message.objects.get(pk = pk)
    if request.user != message.user:
        return HttpResponse("You are not allowed here")
    if request.method == 'POST':
        message.delete()
        return redirect('room', pk = message.room.id)
    context = {'obj':message}
    return render(request, 'base/deleteroom.html',context)

@login_required(login_url='login')
def updateuser(request):
    user = request.user
    if request.method == 'POST':
        form =  UserForm(request.POST,instance = user)
        if form.is_valid():
            form.save()
            return redirect('userprofile', pk = user.id )
    
    form = UserForm(instance = user)
    context  = {'form':form}
    return render(request, 'base/update-user.html',context)

def topiclist(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    topics = Topic.objects.filter(name__icontains=q)
    # rooms = Room.objects.filter(topic__in=topics)
    # rooms_count = rooms.count()
    topics_count = topics.count()
    context = {'topics':topics,'topics_count':topics_count}
    return render(request,'base/topics.html',context)
def activityPage(request):
    room_messages = Message.objects.filter().order_by('-created','-updated')    
    context = {'room_messages':room_messages}
    return render(request,'base/activity.html',context)

