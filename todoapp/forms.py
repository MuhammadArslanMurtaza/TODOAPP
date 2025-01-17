from django import forms
from .models import *

class RegisterForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	phone_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}), required=False)
	
class AccountForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Leave blank if no change'}), required=False)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Leave blank if no change'}), required=False)
	password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Leave blank if no change'}), required=False)
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	phone_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}), required=False)
	about_me = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'id': 'ck-editor-area'}), required=False)

class TODOForm(forms.Form):
	title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	status = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-control'}), required=False)
	description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'id': 'ck-editor-area'}), required=False)
