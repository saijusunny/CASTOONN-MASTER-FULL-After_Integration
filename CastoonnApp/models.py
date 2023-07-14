from django.db import models
from django.contrib.auth.hashers import make_password
# User Registration Section
class User_Registration(models.Model):
    
    name = models.CharField(max_length=255,blank=True,null=True)
    lastname = models.CharField(max_length=255,blank=True,null=True)
    nickname = models.CharField(max_length=255,blank=True,null=True)
    gender = models.CharField(max_length=10,blank=True,null=True)
    date_of_birth = models.DateField(null=True)
    phone_number = models.CharField(max_length=255,blank=True,null=True)
    phone_otp = models.IntegerField(null=True,blank=True)
    email = models.EmailField(blank=True,null=True)
    email_otp =models.IntegerField(null=True,blank=True)
    profession = models.CharField(max_length=255,blank=True,null=True)
    experience = models.IntegerField(null=True)
    role = models.CharField(max_length=255,blank=True,null=True)
    username = models.CharField(max_length=255,blank=True,null=True)
    password = models.CharField(max_length=255,blank=True,null=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def _str_(self):
        return self.nickname
    
    def get_email_field_name(self):
        return 'email'

#Casting Call Creation

class Casting_Call(models.Model):
    user = models.ForeignKey(User_Registration, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255,blank=True,null=True)
    banner = models.ImageField(upload_to='images/casting/banner', null=True, blank=True)
    posting_date =  models.DateField(null=True)
    expired_date =  models.DateField(null=True)
    description = models.TextField(blank=True,null=True)
    location = models.CharField(max_length=255,blank=True,null=True)
    date = models.DateField(null=True)
    production = models.CharField(max_length=255,blank=True,null=True)
    director = models.CharField(max_length=255,blank=True,null=True)
    writter = models.CharField(max_length=255,blank=True,null=True)

class Casting_Call_Role(models.Model):
    user = models.ForeignKey(User_Registration, on_delete=models.SET_NULL, null=True, blank=True)
    casting = models.ForeignKey(Casting_Call, on_delete=models.SET_NULL, null=True, blank=True)
    role_title = models.CharField(max_length=255,blank=True,null=True)
    role_description = models.TextField(blank=True,null=True)

# contest creation
class Contest(models.Model):
    title = models.CharField(max_length=255,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    audio = models.FileField(upload_to='images/contest/audio', blank=True)
    status = models.CharField(max_length=255,blank=True,null=True)
    posting_date = models.DateField(null=True)