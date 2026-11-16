from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BooktableForm(forms.ModelForm):
    Booking_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Booktable
        fields = ['Name', 'phn_no', 'Email', 'Total_persons', 'Booking_date']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['Name', 'Email', 'Message','rating']



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=True)
    place = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'gender', 'place', 'password1', 'password2']

