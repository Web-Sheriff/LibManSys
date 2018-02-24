from django import forms

from .models import User

class LoginForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('login','password')
		exclude = [""]

class SignUpForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('login','password','first_name','second_name','address','phone_number')
		exclude = [""]
