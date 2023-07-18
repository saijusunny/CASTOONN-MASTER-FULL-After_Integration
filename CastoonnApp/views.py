from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib import messages

from django.conf import settings
from django.core.mail import send_mail
import uuid
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth import update_session_auth_hash

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
            if Profile_artist.objects.filter(user_id=member.id).exists():
                return redirect('user_type')
            else:
                return redirect('artist_profile_view')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request,'index/login.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if  User_Registration.objects.filter(email=email).exists():
            user =  User_Registration.objects.get(email=email)

        

            current_site = get_current_site(request)
            mail_subject = "Reset your password"
            message = render_to_string('index/forget-password/reset_password_email.html',{
                'user':user,
                'domain' :current_site,
                'user_id' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            }) 

            to_email = email
            send_email = EmailMessage(mail_subject,message,to = [to_email])
            send_email.send()

            messages.success(request,"Password reset email has been sent your email address.")
            return redirect('login_main')
        else:
            messages.error(request,"This account does not exists !")
            return redirect('forgotPassword')
    return render(request,'index/forget-password/forgotPassword.html')


def resetpassword_validate(request,uidb64,token):
    try:
        user_id = urlsafe_base64_decode(uidb64).decode()
        user =  User_Registration._default_manager.get(pk=user_id)  
    except(TypeError,ValueError,OverflowError, User_Registration.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['user_id'] = user_id 
        messages.success(request,"Please reset your password.")
        return redirect('resetPassword')
    else:
        messages.error(request,"The link has been expired !")
        return redirect('login_main')
    
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('user_id') 
            user =  User_Registration.objects.get(pk=uid)
            user.password = password
            user.save()
            messages.success(request,"Password reset successfull.")
            return redirect('login_main')

        else:
            messages.error(request,"Password do not match")
            return redirect('resetPassword')
    else:
        return render(request,'index/forget-password/resetPassword.html')

######################################################################### <<<<<<<<<< CREATOR MODULE >>>>>>>>>>>>>>



######################################################################### <<<<<<<<<< ARTIST MODULE >>>>>>>>>>>>>>>>
def artist_profile_view(request):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    if request.method == 'POST':
        
        firstname = request.POST.get('firstname',None)
        lastname = request.POST.get('lastname',None)
        phonenumber = request.POST.get('phonenumber',None)
        email = request.POST.get('email',None)
        gender = request.POST.get('gender',None)
        date_of_birth = request.POST.get('date_of_birth',None)
        marital_status = request.POST.get('marital_status',None)
        profection = request.POST.get('profection',None)
        height = request.POST.get('height',None)
        weight = request.POST.get('weight',None)
        interests = request.POST.get('interests',None)
        hobbies = request.POST.get('hobbies',None)
        passions = request.POST.get('passions',None)
        goals = request.POST.get('goals',None)
        achievements = request.POST.get('achievements',None)
        social_media_links = request.POST.get('social_media_links',None)
        skills = request.POST.get('skills',None)
        awards = request.POST.get('awards',None)
        message = request.POST.get('message',None)
        
        profile_artist = Profile_artist(
            firstname=firstname,
            lastname=lastname,
            phonenumber=phonenumber,
            email=email,
            gender=gender,
            date_of_birth=date_of_birth,
            marital_status=marital_status,
            profection=profection,
            height=height,
            weight=weight,
            interests=interests,
            hobbies=hobbies,
            passions=passions,
            goals=goals,
            achievements=achievements,
            social_media_links=social_media_links,
            skills=skills,
            awards=awards,
            message=message,
            user=usr
        )
        profile_artist.save()


        return redirect('user_type')
    context={
        'user':usr
    }
    return render(request,'artist/profile_artist.html', context)


def logout(request):
    if 'userid' in request.session:  
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/')