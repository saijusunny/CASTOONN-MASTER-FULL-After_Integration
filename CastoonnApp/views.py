from django.shortcuts import render, redirect


######################################################################### <<<<<<<<<< LANDING MODULE >>>>>>>>>>>>>>
def index(request):
    return render(request, 'index/index.html')

def login_main(request):
    return render(request,'index/login.html')

def user_type(request):
    return render(request, 'index/user_type.html')



######################################################################### <<<<<<<<<< CREATOR MODULE >>>>>>>>>>>>>>



######################################################################### <<<<<<<<<< ARTIST MODULE >>>>>>>>>>>>>>>>

