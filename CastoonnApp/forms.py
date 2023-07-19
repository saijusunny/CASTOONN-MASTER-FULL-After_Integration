from django import forms
from .models import User_Registration
from django.core.exceptions import ValidationError
import re
from django.core.validators import EmailValidator
from django.contrib import messages

########################################################<<<<<<<<< Creator Userform >>>>>>>>>>>>>>>>>

class User_RegistrationForm(forms.ModelForm):

        gender = forms.ChoiceField(choices=[
            ('Gender', 'Gender'),
            ('Female', 'Female'),
            ('Male', 'Male'),
            ('Other', 'Other'),
        ], widget=forms.Select(attrs={'class': 'form-control item', 'id': 'Gender', 'placeholder': 'Gender'}))
        
        # profession = forms.ChoiceField(choices=[
        #     ('Profession', 'Profession'),
        #     ('Actor', 'Actor'),
        #     ('Costume_Designer', 'Costume_Designer'),
            
        # ], widget=forms.Select(attrs={'class': 'form-control item', 'id': 'profession', 'placeholder': 'Profession'}))
        
        date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control item', 'id': 'birthday', 'placeholder': 'Date of Birth'}))

        class Meta:
            model = User_Registration
            fields = '__all__'
        
            widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control item','placeholder':'Name'}),
                'lastname': forms.TextInput(attrs={'class': 'form-control item','placeholder':'Lastname'}),
                'nickname': forms.TextInput(attrs={'class': 'form-control item','placeholder':'Nickname'}),
                'phone_number': forms.TextInput(attrs={'class': 'form-control item','placeholder':'phone number'}),
                
                'phone_otp': forms.TextInput(attrs={'class': 'form-control item','placeholder':'Enter phone OTP'}),
                'email': forms.EmailInput(attrs={'class': 'form-control item','placeholder':'Email','id':'email'}),
                'email_otp': forms.TextInput(attrs={'class': 'form-control item','placeholder':'Enter Email OTP','id':'email_otp'}),
                'experience': forms.NumberInput(attrs={'class': 'form-control item','placeholder':'Experience'}),
                'role': forms.HiddenInput(attrs={'value': 'PREFIX_VALUE','id': 'role-field'}),
                'profession' : forms.TextInput(attrs={'class': 'form-control item','placeholder':'profession'}),

                }
            
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['username'].required = False
            self.fields['password'].required = False