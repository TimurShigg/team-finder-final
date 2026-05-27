# projects/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from .models import Project
from .forms import ProjectForm


def project_list_view(request):
    # Получаем все проекты от новых к старым
    projects_qs = Project.objects.all().order_by('-created_at')

    # Пагинация (12 проектов на страницу)
    paginator = Paginator(projects_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # В ТЗ просят передать "projects", но для пагинации в шаблонах часто нужен page_obj
    return render(request, 'projects/project_list.html', {
        'page_obj': page_obj,
        'projects': page_obj  # дублируем для совместимости с шаблоном
    })


def project_detail_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
def project_create_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            # Добавляем создателя в участники
            project.participants.add(request.user)
            return redirect('projects:project_detail', project_id=project.id)
    else:
        form = ProjectForm()

    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})


@login_required
def project_edit_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Редактировать может только автор
    if request.user != project.owner:
        return redirect('projects:project_detail', project_id=project.id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': True})


@login_required
@require_POST
def project_complete_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user == project.owner and project.status == 'open':
        project.status = 'closed'
        project.save()
        return JsonResponse({"status": "ok", "project_status": "closed"})

    return JsonResponse({"error": "Forbidden or already closed"}, status=403)


@login_required
@require_POST
def project_toggle_participate_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user in project.participants.all():
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)

    return JsonResponse({"status": "ok"})
