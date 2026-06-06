from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Project(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("closed", "Closed"),
    ]

    name = models.CharField(max_length=200, verbose_name="Название проекта")
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание проекта"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="Автор проекта",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    github_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на GitHub")
    status = models.CharField(
        max_length=6, choices=STATUS_CHOICES, default="open", verbose_name="Статус"
    )
    participants = models.ManyToManyField(
        User, related_name="participated_projects", blank=True, verbose_name="Участники"
    )

    def __str__(self):
        return self.name
