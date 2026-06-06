from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    path("list/", views.project_list_view, name="project_list"),
    path("create-project/", views.project_create_view, name="create_project"),
    path("<int:project_id>/", views.project_detail_view, name="project_detail"),
    path("<int:project_id>/edit/", views.project_edit_view, name="edit_project"),
    path(
        "<int:project_id>/complete/",
        views.project_complete_view,
        name="complete_project",
    ),
    path(
        "<int:project_id>/toggle-participate/",
        views.project_toggle_participate_view,
        name="toggle_participate",
    ),
]
