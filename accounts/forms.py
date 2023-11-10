from django import forms

class LoginForm(forms.Form):
    student_id = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)