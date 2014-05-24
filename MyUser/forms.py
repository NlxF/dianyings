#coding:utf-8
__author__ = 'ISM'
from django import forms
from django.contrib import auth
from django.utils.translation import ugettext as _
from MyUser.models import MyUser


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=25)
    email = forms.EmailField(min_length=6)
    password1 = forms.CharField(widget=forms.PasswordInput, min_length=6)
    password2 = forms.CharField(widget=forms.PasswordInput, min_length=6)

    def clean_username(self):
        """验证username是否重复、格式是否正确"""
        if not self.cleaned_data['username'].replace('_', '').isalnum():
            raise forms.ValidationError(_('InvalidValue: %(value)s'),
                                        code=44,
                                        params={'value': _('Username wrong format')})
        username = MyUser.objects.filter(username=self.cleaned_data['username'])
        if not username:
            return self.cleaned_data['username']
        raise forms.ValidationError(
            _('InvalidValue: %(value)s'),
            code=42,
            params={'value': _('Username has been used')}
        )

    def clean_email(self):
        """验证email是否重复"""
        emails = MyUser.objects.filter(email=self.cleaned_data['email'])

        if not emails:
            return self.cleaned_data['email']
        raise forms.ValidationError(_('InvalidValue: %(value)s'),
                                    code=40,
                                    params={'value': 'E-mail has been used'}
        )

    def clean_password2(self):
        """验证2次密码是否正确"""
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('InvalidValue: %(value)s'),
                                        code=41, params={"value": 'Passwords do not match'}
            )
        return password2


class SettingForm(forms.Form):
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    old_password = forms.CharField(required=False)
    password1 = forms.CharField(required=False)
    password2 = forms.CharField(required=False)
    file = forms.FileField(required=False)

    user = None

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password', "")
        if old_password:
            exist = auth.authenticate(username=self.cleaned_data['username'], password=old_password)
            if exist:
                return old_password
            raise forms.ValidationError(_('InvalidValue: %(value)s'),
                                        code=43, params={"value": _('old password is incorrect')}
            )
        return old_password

    def clean_password2(self):
        """验证2次密码是否正确"""
        password1 = self.cleaned_data.get('password1', "")
        password2 = self.cleaned_data.get('password2', "")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                _('InvalidValue: %(value)s'),
                code=41, params={"value": _('Passwords do not match')}
            )
        elif password1 and password2 and not self.cleaned_data.get('old_password', ''):
            raise forms.ValidationError(
                _('InvalidValue: %(value)s'),
                code=41,
                params={"value": _('old Passwords need right')}
            )
        return password2

    def clean_username(self):
        """验证username是否重复"""
        username = self.cleaned_data.get('username', "")
        if username:
            exist = MyUser.objects.filter(username=username)
            if not exist or self.user in exist:
                return username
            raise forms.ValidationError(_('InvalidValue: %(value)s'),
                                        code=42,
                                        params={'value': "Username has been used!!"}
            )
        return username

    def clean_email(self):
        """验证email是否重复"""
        email = self.cleaned_data.get('email', "")
        if email:
            exist = MyUser.objects.filter(email=email)
            if not exist or self.user in exist:
                return email
            raise forms.ValidationError(_('InvalidValue: %(value)s'),
                                        code=40,
                                        params={'value': "E-mail has been used"}
            )
        return email
