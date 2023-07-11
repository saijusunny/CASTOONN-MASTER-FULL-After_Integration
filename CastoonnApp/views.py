from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib import messages

######################################################################### <<<<<<<<<< LANDING MODULE >>>>>>>>>>>>>>
def index(request):
    return render(request, 'index/index.html')



def user_type(request):
    print(request.session['userid'])
    return render(request, 'index/user_type.html')

def login_main(request):
    if request.method == 'POST':
        username  = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            return redirect('user_type')
        
        if User_Registration.objects.filter(username=request.POST['username'], password=request.POST['password'],role="user1").exists():

            member = User_Registration.objects.get(username=request.POST['username'],password=request.POST['password'])
            
            request.session['userid'] = member.id
            
            return redirect('user_type')


       

        elif User_Registration.objects.filter(username=request.POST['username'], password=request.POST['password'],role="user2").exists():
            member = User_Registration.objects.get(username=request.POST['username'],password=request.POST['password'])
            request.session['userid'] = member.id

            return redirect('user_type')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request,'index/login.html')

######################################################################### <<<<<<<<<< CREATOR MODULE >>>>>>>>>>>>>>



######################################################################### <<<<<<<<<< ARTIST MODULE >>>>>>>>>>>>>>>>

