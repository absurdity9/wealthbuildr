from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import FModel, Income, Expense, Asset, PublishedPage
from django.forms import formset_factory

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)

class FModelForm(forms.ModelForm):
    class Meta:
        model = FModel
        fields = ['fmodel_name']

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['fmodel', 'income_name', 'value']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['fmodel', 'expense_name', 'value']