from django.urls import re_path,path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    ###################################################################################<<<<<<<<< LANDING MODULE >>>>>>>>>>>>>>>>>
    path('', views.index, name='index'),
    path('user_type', views.user_type, name='user_type'),
    path('login_main',views.login_main, name='login_main'),

    ################################################################################### <<<<<<<<< CREATOR MODULE >>>>>>>>>>>>>>>>>
    
    

    ################################################################################### <<<<<<<<< Artist MODULE >>>>>>>>>>>>>>>>>
    


    
    ]