# users/views.py
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import User, Skill
from .forms import UserRegistrationForm, UserLoginForm, UserEditProfileForm


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('projects:project_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('projects:project_list')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('projects:project_list')


def user_list_view(request):
    users = User.objects.all().order_by('id')

    # ТЗ Вариант 2: Фильтрация по навыкам
    skill_name = request.GET.get('skill')
    active_skill = None
    if skill_name:
        users = users.filter(skills__name=skill_name).distinct()
        active_skill = skill_name

    paginator = Paginator(users, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Получаем все уникальные имена навыков для панели фильтров
    all_skills = Skill.objects.values_list('name', flat=True).distinct().order_by('name')

    context = {
        'page_obj': page_obj,
        'all_skills': all_skills,
        'active_skill': active_skill,
        'query_prefix': f'skill={skill_name}&' if skill_name else ''
    }
    return render(request, 'users/participants.html', context)


def user_detail_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/user-details.html', {'user': user})


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserEditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:user_detail', user_id=request.user.id)
    else:
        form = UserEditProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form, 'user': request.user})


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'users/change-password.html'

    def get_success_url(self):
        return reverse_lazy('users:user_detail', kwargs={'user_id': self.request.user.id})


# --- API для Навыков (Автодополнение, Добавление, Удаление) ---

def skills_autocomplete_view(request):
    q = request.GET.get('q', '')
    if q:
        # ТЗ: навыки, которые начинаются с подстроки q (istartswith вместо icontains)
        skills = Skill.objects.filter(name__istartswith=q).order_by('name')[:10]
        results = [{"id": skill.id, "name": skill.name} for skill in skills]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)


@login_required
@require_POST
def add_skill_view(request, user_id):
    if request.user.id != user_id:
        return JsonResponse({"error": "Forbidden"}, status=403)

    try:
        # Универсальное чтение данных (и для JSON, и для FormData)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.POST

        skill_id = data.get('skill_id')
        name = data.get('name')

        created = False
        added = False
        skill = None

        if skill_id:
            skill = get_object_or_404(Skill, id=skill_id)
        elif name:
            skill, created = Skill.objects.get_or_create(name=name.strip())

        if skill and not request.user.skills.filter(id=skill.id).exists():
            request.user.skills.add(skill)
            added = True

        return JsonResponse({
            "skill_id": skill.id if skill else None,
            "name": skill.name if skill else None,
            "created": created,
            "added": added
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@login_required
@require_POST
def remove_skill_view(request, user_id, skill_id):
    if request.user.id != user_id:
        return JsonResponse({"error": "Forbidden"}, status=403)

    skill = get_object_or_404(Skill, id=skill_id)
    if request.user.skills.filter(id=skill.id).exists():
        request.user.skills.remove(skill)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "Not found"}, status=404)
