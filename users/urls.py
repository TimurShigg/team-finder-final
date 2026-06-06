from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("list/", views.user_list_view, name="user_list"),
    path("edit-profile/", views.edit_profile_view, name="edit_profile"),
    path(
        "change-password/",
        views.UserPasswordChangeView.as_view(),
        name="change_password",
    ),
    path("<int:user_id>/", views.user_detail_view, name="user_detail"),
    path("skills/", views.skills_autocomplete_view, name="skills_autocomplete"),
    path("<int:user_id>/skills/add/", views.add_skill_view, name="add_skill"),
    path(
        "<int:user_id>/skills/<int:skill_id>/remove/",
        views.remove_skill_view,
        name="remove_skill",
    ),
]
