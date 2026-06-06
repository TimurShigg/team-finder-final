import random
from io import BytesIO
from PIL import Image, ImageDraw

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.files.base import ContentFile


class Skill(models.Model):
    name = models.CharField(max_length=124, verbose_name='Название навыка')

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('Электронная почта обязательна')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, surname=surname, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, surname, phone, password, **extra_fields)


def generate_avatar(text):
    """Функция генерирует аватарку с первой буквой имени на случайном фоне"""
    colors = ['#1abc9c', '#2ecc71', '#3498db', '#9b59b6', '#34495e', '#16a085', '#27ae60', '#2980b9', '#8e44ad',
              '#2c3e50', '#f1c40f', '#e67e22', '#e74c3c', '#d35400', '#c0392b']
    bg_color = random.choice(colors)

    img = Image.new('RGB', (200, 200), color=bg_color)
    d = ImageDraw.Draw(img)

    d.text((80, 80), text.upper(), fill=(255, 255, 255))

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f'avatar_{text}.png')


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=124, verbose_name='Имя')
    surname = models.CharField(max_length=124, verbose_name='Фамилия')
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватарка')
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    github_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на GitHub')
    about = models.TextField(max_length=256, blank=True, null=True, verbose_name='О себе')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='Администратор')

    skills = models.ManyToManyField(Skill, related_name='users', blank=True, verbose_name='Навыки')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone']

    def save(self, *args, **kwargs):
        if not self.avatar and self.name:
            self.avatar = generate_avatar(self.name[0])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.surname}"
