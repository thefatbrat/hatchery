from django import forms
from django.core.validators import *

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    age = forms.IntegerField(validators=[MinValueValidator(20),
                                         MaxValueValidator(100)])
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    gender_2 = forms.ChoiceField(choices=GENDER_CHOICES,
                               widget=forms.RadioSelect)

