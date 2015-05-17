
__author__ = 'aamirbhatt'

from django import forms
from api import UserInstanceResource


class LoginForm(forms.Form):
    """Login Form for all users"""

    email = forms.EmailField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Email',
               'class': 'login-user-input',
               'id': 'email',
               'onfocus': "this.placeholder = ''",
               'onblur': "this.placeholder = 'Email'"}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'password',
               'class': 'login-pass-input',
               'id': 'password',
               'onfocus': "this.placeholder = ''",
               'onblur': "this.placeholder = 'password'"}))


class SignUpForm(forms.Form):
    '''file are uploaded using this form'''
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Email',
                                      'class': 'form-control',
                                      'id': 'email',
                                      'onfocus': "this.placeholder = ''",
                                      'onblur': "this.placeholder = 'Email'"}),
        required=True)
    password = forms.CharField(
        label=("Password"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                          'class': "form-control"})
    )
    password_confirm = forms.CharField(
        label=("Password (again)"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Re-type Password',
                                          'class': "form-control"}))


    def clean_email(self):
        email = self.cleaned_data["email"]
        user = UserInstanceResource()._filter(email=email)
        if user:
            raise forms.ValidationError(
                ("A user is registered with this email address."))
        return email

    def clean(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data[
                "password_confirm"]:
                raise forms.ValidationError(
                    ("You must type the same password each time."))
        return self.cleaned_data

class UserEditForm(forms.Form):
    '''file are uploaded using this form'''
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '',
                                      'class': 'form-control',
                                      'id': 'email',
                                      'onfocus': "this.placeholder = ''",
                                      'onblur': "this.placeholder = ''"}),
        required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '',
                                                              'class': 'form-control',
                                                              'id': 'email',
                                                              'onfocus': "this.placeholder = ''",
                                                              'onblur': "this.placeholder = ''"}),
                                required=True)
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': '',
               'class': 'form-control',
               'id': 'password',
               'onfocus': "this.placeholder = ''",
               'onblur': "this.placeholder = ''"}), required=False)


class PasswordResetTokenForm(forms.Form):
    '''password reset change password is here'''
    password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(render_value=False,
                                   attrs={
                                       'placeholder': 'Password',
                                       'class': 'login-user-input',
                                       'required': 'required'
                                   })

    )
    password_confirm = forms.CharField(
        label="New Password (again)",
        widget=forms.PasswordInput(render_value=False,
                                   attrs={
                                       'placeholder': 'Confirm Password',
                                       'class': 'login-user-input',
                                   })
    )


    def clean_password_confirm(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data[
                "password_confirm"]:
                raise forms.ValidationError("Your passwords dont match")
            password = self.cleaned_data["password"]
        return self.cleaned_data["password_confirm"]