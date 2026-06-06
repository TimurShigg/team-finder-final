from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Project

User = get_user_model()


class ProjectViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.owner = User.objects.create_user(
            email='owner@example.com', name='Owner', surname='Test', phone='89991112233', password='pass'
        )
        self.other_user = User.objects.create_user(
            email='other@example.com', name='Other', surname='Test', phone='89992223344', password='pass'
        )

        # Создаем проект
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            owner=self.owner
        )

    def test_create_project_adds_owner_to_participants(self):
        """При создании проекта автор должен стать его участником"""
        self.client.force_login(self.owner)
        url = reverse('projects:create_project')
        response = self.client.post(url, data={
            'name': 'New Project',
            'description': 'Desc',
            'status': 'open'
        })

        self.assertEqual(response.status_code, 302)
        new_project = Project.objects.get(name='New Project')
        self.assertEqual(new_project.owner, self.owner)
        self.assertIn(self.owner, new_project.participants.all())

    def test_edit_project_allowed_for_owner(self):
        """Владелец может редактировать проект"""
        self.client.force_login(self.owner)
        url = reverse('projects:edit_project', kwargs={'project_id': self.project.id})
        response = self.client.post(url, data={
            'name': 'Updated Name',
            'status': 'closed'
        })

        self.project.refresh_from_db()
        self.assertEqual(self.project.name, 'Updated Name')
        self.assertEqual(self.project.status, 'closed')
        self.assertEqual(response.status_code, 302)

    def test_edit_project_forbidden_for_other_user(self):
        """Не владелец при попытке редактирования должен быть перенаправлен (ограничение доступа)"""
        self.client.force_login(self.other_user)
        url = reverse('projects:edit_project', kwargs={'project_id': self.project.id})
        response = self.client.post(url, data={'name': 'Hacked Name'})

        self.assertRedirects(response, reverse('projects:project_detail', kwargs={'project_id': self.project.id}))
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, 'Test Project')

    def test_toggle_participate(self):
        """Проверка добавления и удаления из участников (AJAX POST)"""
        self.client.force_login(self.other_user)
        url = reverse('projects:toggle_participate', kwargs={'project_id': self.project.id})

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.other_user, self.project.participants.all())

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.other_user, self.project.participants.all())

    def test_complete_project_view(self):
        """Проверка закрытия проекта автором"""
        self.client.force_login(self.owner)
        url = reverse('projects:complete_project', kwargs={'project_id': self.project.id})

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

        self.project.refresh_from_db()
        self.assertEqual(self.project.status, 'closed')
