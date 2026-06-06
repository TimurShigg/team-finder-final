import re
import random
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        random_tail = random.randint(1000000000, 9999999999)
        user.phone = f'8{random_tail}'
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'autofocus': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            del self.fields['username']

    def clean(self):
        email = self.cleaned_data.get('email')
        if email:
            self.cleaned_data['username'] = email
        return super().clean()


class UserEditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'about', 'phone', 'github_url']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone

        clean_phone = re.sub(r'[\s\-()]', '', phone)

        if not re.match(r'^(8|\+7)\d{10}$', clean_phone):
            raise forms.ValidationError("Номер телефона должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX")

        if clean_phone.startswith('8'):
            clean_phone = '+7' + clean_phone[1:]

        if User.objects.filter(phone=clean_phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Пользователь с таким номером телефона уже существует.")

        return clean_phone

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url and not url.startswith('https://github.com/'):
            raise forms.ValidationError("Ссылка должна вести на GitHub (https://github.com/...)")
        return url
