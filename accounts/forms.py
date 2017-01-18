__author__ = 'carlos'
from django import forms
from django.forms.widgets import PasswordInput

TOPIC_CHOICES = (
    ('Internet', 'Internet'),
    ('Correo', 'Correo'),
    ('Chat', 'Chat'),
    ('Dominio', 'Dominio'),
    ('Ftp', 'Ftp'),
    ('Default', 'Default'),
)

class ContactForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nombre de Ususario'}))
    old_password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}), max_length=100);
    new_password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'New Password'}), max_length=100);
    repeat_password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Repeat Password'}), max_length=100);
    service = forms.ChoiceField(choices=TOPIC_CHOICES);