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
from .forms import *
import random
import string
from django.http import HttpResponse
from django.http import JsonResponse
import json
from datetime import datetime, timedelta
######################################################################### <<<<<<<<<< LANDING MODULE >>>>>>>>>>>>>>
def index(request):
    return render(request, 'index/index.html')



def user_type(request):

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
def logout(request):
    if 'userid' in request.session:  
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/')
############################################################# <<<<<<<<<< CREATOR MODULE >>>>>>>>>>>>>>
def creator_registration(request):

    if request.method =='POST':
        form = User_RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            lastname = form.cleaned_data['lastname']
            nickname = form.cleaned_data['nickname']
            gender = form.cleaned_data['gender']
            profession = form.cleaned_data['profession']
            date_of_birth = form.cleaned_data['date_of_birth']
            phone_number = form.cleaned_data['phone_number']
            phone_otp = form.cleaned_data['phone_otp']
            email = form.cleaned_data['email']
            email_otp = form.cleaned_data['email_otp']
            experience = form.cleaned_data['experience']
            role = form.cleaned_data['role']
            
            if User_Registration.objects.filter(email=email).exists():
                messages.error(request, 'Email Id already exists')
                return redirect('creator_registration')
            else:
                
                user_registration = User_Registration(
                    name=name,
                    lastname=lastname,
                    nickname=nickname,
                    gender=gender,
                    profession=profession,
                    date_of_birth=date_of_birth,
                    phone_number=phone_number,
                    phone_otp=phone_otp,
                    email=email,
                    email_otp=email_otp,
                    experience=experience,
                    role=role
                )
                user_registration.save()
                user_id = user_registration.pk
            return redirect('index_creator_confirmation',user_id=user_id)
    else:
        form = User_RegistrationForm()
        form.initial['role'] = 'user1'
    return render(request,'index\index_creator\index_creator_registraion.html',{'form':form})



def index_creator_confirmation(request,user_id):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User_Registration.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('index_creator_confirmation', user_id=user_id)
            else:
                creator_object = get_object_or_404(User_Registration, pk=user_id)
                creator_object.username=username
                creator_object.password = password
                creator_object.save()
                messages.success(request, 'Thank you for registering with us.')
            return redirect('login_main')
        else:
            messages.error(request, ' Password and Confirm Password are not matching. Please verify it.')
            return redirect('index_creator_confirmation', user_id=user_id)

    return render(request,'index\index_creator\index_creator_confirmation.html',{'user_id':user_id})


#<<<<<<<<<< Email Verification >>>>>>>>>>>>>>
def email_send(request):
    digits = string.digits
    otp = ''.join(random.choices(digits, k=6))
    email = request.GET.get('inputValue')
    user_email = Email_Validation.objects.create(email_temp=email,email_otp_temp=otp)
    user_email.save()
    subject = 'Catoonn Email Verification OTP'
    message = f'Hi {email},\nYour Email Verification OTP is: {otp}'
    from_email = 'email'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def verify_email_otp(request):
    email=request.GET.get('emailValue')
    otp=request.GET.get('otpValue')
    print(otp)
    print(email)
    instance = get_object_or_404(Email_Validation,email_otp_temp=otp)
    if instance.email_temp == email:
        result="Email Verified"
    else:
        result="Your Entered Otp Is Incorrect"
    print(result)
    return JsonResponse({"status": " not", 'result':result})



########################################################## <<<<<<<<<< ARTIST MODULE >>>>>>>>>>>>>>>>

def artist_registration(request):

    if request.method =='POST':
        form = User_RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User_Registration.objects.filter(email=email).exists():
                messages.error(request, 'Email Id already exists')
                return redirect('artist_registration')
            else:
                user_model=form.save()
                user_id = user_model.pk
                return redirect('index_artist_confirmation',user_id=user_id)
    else:
        form = User_RegistrationForm()
        form.initial['role'] = 'user2'
    return render(request,'index\index_artist\index_artist_registraion.html',{'form':form})


def index_artist_confirmation(request,user_id):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            print("success")
            if User_Registration.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('index_artist_confirmation', user_id=user_id)
            else:
                artist_object = get_object_or_404(User_Registration, pk=user_id)
                artist_object.username=username
                artist_object.password = password
                artist_object.save()
                messages.success(request, 'Thank you for registering with us.')
                return redirect('login_main')
        else:
            messages.error(request, ' Password and Confirm Password are not matching. Please verify it.')
            return redirect('index_artist_confirmation', user_id=user_id)

    return render(request,'index\index_artist\index_artist_confirmation.html',{'user_id':user_id})
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

# subscription Plans
def subscription_plan(request):
    plans = SubscriptionPlan.objects.all()
    context = {'plans': plans,'selected_plan':'Boost'}
    return render(request, 'artist/artist_subscription.html', context)

def subscription_plan_profile(request):
    plans = SubscriptionPlan.objects.all()
    context = {'plans': plans,'selected_plan':'Boost'}
    return render(request, 'artist/artist_subscription_profile.html', context)

def process_payment(request):
    if request.session.has_key('userid'):
        pass
    else:
        return redirect('/')
    ids=request.session['userid']
    usr=User_Registration.objects.get(id=ids)
    if request.method == "POST":
     
        # try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        plan = data.get('plan')
        amount = data.get('amount')
        start_date = datetime.now().date()
        print(plan)
        if plan == '199 1 month':
            end_date = start_date + timedelta(days=30)
        elif plan == '499 3 months':
            end_date = start_date + timedelta(days=90)
        elif plan == '799 6 months':
            end_date = start_date + timedelta(days=180)
        else:
            return JsonResponse({'message': 'Invalid plan selection'}, status=400)
        
        payment = Payment.objects.create(
            user=usr,
            plan=plan,
            amount=amount,
            start_date=start_date,
            end_date=end_date
        )
        
        # Return a JSON response indicating the success of the payment processing
        return JsonResponse({'message': 'Payment successful'})
        # except Exception as e:
        #     return JsonResponse({'message': 'Error processing payment', 'error': str(e)}, status=400)
    else:
        # Handle invalid request methods
        return JsonResponse({'message': 'Invalid request method'}, status=400)

