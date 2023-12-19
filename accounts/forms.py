from django import forms
# from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class SuperAdminUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=[('Super Admin', 'Super Admin')], widget=forms.Select())

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']


class CashierUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=[('Cashier', 'Cashier')], widget=forms.Select())

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']


class PasswordChangeForm(forms.Form): # User Change Password Form
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


