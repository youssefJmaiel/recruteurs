# recruitment/forms.py

from django import forms
from .models import CV
from django.contrib.auth.models import User

class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['user', 'title', 'cv_file']  # Assurez-vous que 'title' et 'file' sont inclus ici


# class CVForm(forms.ModelForm):
#     class Meta:
#         model = CV
#         fields = ['title', 'cv_file']  # Use the correct field name from the model


class CVUploadForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['cv_file']



class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']