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

class Email_Validation(models.Model):
    email_temp = models.EmailField()
    email_otp_temp =models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.email_temp + " " + str(self.email_otp_temp) 

# Create Artist Profile
class Profile_artist(models.Model):
    user = models.ForeignKey(User_Registration, on_delete=models.SET_NULL, null=True, blank=True)
    firstname = models.CharField(max_length=255,blank=True,null=True)
    lastname = models.CharField(max_length=255,blank=True,null=True)
    phonenumber = models.CharField(max_length=20)
    email = models.EmailField()
    gender = models.CharField(max_length=255,blank=True,null=True)
    date_of_birth = models.DateField(null=True)
    marital_status = models.CharField(max_length=255,blank=True,null=True)
    profection = models.CharField(max_length=255,blank=True,null=True)
    height = models.IntegerField(null=True,blank=True)
    weight = models.IntegerField(null=True,blank=True)
    interests = models.TextField(blank=True,null=True)
    hobbies = models.TextField(blank=True,null=True)
    passions = models.TextField(blank=True,null=True)
    goals = models.TextField(blank=True,null=True)
    achievements = models.TextField(blank=True,null=True)
    social_media_links = models.TextField(blank=True,null=True)
    skills = models.TextField(blank=True,null=True)
    awards = models.TextField(blank=True,null=True)
    message = models.TextField(blank=True,null=True)

    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100,null=True)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2,null=True)

    def __str__(self):
        return self.name

class Payment(models.Model):
    user = models.ForeignKey(User_Registration, on_delete=models.CASCADE,null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    plan = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Payment ID: {self.id}"

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