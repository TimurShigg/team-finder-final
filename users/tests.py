import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Skill
from .forms import UserEditProfileForm

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user_generates_avatar(self):
        """Проверка, что при создании пользователя без аватарки, она генерируется автоматически"""
        user = User.objects.create_user(
            email='test@example.com',
            name='Иван',
            surname='Иванов',
            phone='89991234567',
            password='password123'
        )
        self.assertTrue(user.avatar.name.startswith('avatars/avatar_И'))


class UserFormTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com', name='A', surname='B', phone='+79990001122', password='123'
        )

    def test_valid_phone_format(self):
        """Проверка правильного формата телефона"""
        form_data = {
            'name': 'A', 'surname': 'B', 'phone': '89991112233'
        }
        form = UserEditProfileForm(data=form_data, instance=self.user1)

        self.assertTrue(form.is_valid(), form.errors)

        self.assertEqual(form.cleaned_data['phone'], '+79991112233')

    def test_invalid_phone_format(self):
        """Проверка неправильного формата телефона"""
        form_data = {'name': 'A', 'surname': 'B', 'phone': '12345'}
        form = UserEditProfileForm(data=form_data, instance=self.user1)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_duplicate_phone(self):
        """Проверка уникальности номера телефона"""
        User.objects.create_user(
            email='user2@example.com', name='C', surname='D', phone='+79999999999', password='123'
        )
        form_data = {'name': 'A', 'surname': 'B', 'phone': '89999999999'}
        form = UserEditProfileForm(data=form_data, instance=self.user1)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['phone'][0], "Пользователь с таким номером телефона уже существует.")


class UserSkillAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='api@example.com', name='API', surname='Test', phone='89991234567', password='pass'
        )
        self.client.force_login(self.user)

    def test_add_new_skill(self):
        """Тест добавления нового навыка пользователю (JSON POST)"""
        url = reverse('users:add_skill', kwargs={'user_id': self.user.id})
        response = self.client.post(url, data=json.dumps({'name': 'Python'}), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Skill.objects.filter(name='Python').exists())
        self.assertTrue(self.user.skills.filter(name='Python').exists())

    def test_add_skill_forbidden_for_other_user(self):
        """Нельзя добавить навык другому пользователю"""
        other_user = User.objects.create_user(
            email='other@example.com', name='O', surname='T', phone='89990000000', password='123'
        )
        url = reverse('users:add_skill', kwargs={'user_id': other_user.id})
        response = self.client.post(url, data=json.dumps({'name': 'Java'}), content_type='application/json')

        self.assertEqual(response.status_code, 403)
