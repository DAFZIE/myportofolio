import datetime
from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.models import Experience, Project, Education
from main.forms import ProjectForm, ExperienceForm, EducationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.http import require_POST


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie(
            "last_login", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        return response

    context = {
        "name": "Daffa Akmal Mahadaya Pasaribu",
        "name_short": "Daffa",
        "form": form,
    }
    return render(request, "login.html", context)


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Daffa Akmal Mahadaya Pasaribu",
        "name_short": "Daffa",
        "form": form,
    }
    return render(request, "register.html", context)


def show_main(request):
    last_login = request.COOKIES.get(
        "last_login", "Belum ada sesi login / Cookie tidak ditemukan"
    )
    context = {
        "name": "Daffa Akmal Mahadaya Pasaribu",
        "name_short": "Daffa",
        "npm": "2506584451",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Just another furry that studies in compsci "
            "and is trying to live his life to the fullest."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    json_response = get_experience_json(request)

    experience = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experience = [experience.object for experience in experience]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Daffa Akmal Mahadaya Pasaribu",
        "name_short": "Daffa",
        "experience_list": experience,
        "title_query": title_query,
    }
    return render(request, "experience.html", context)


def show_project(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Daffa Akmal Mahadaya Pasaribu",
        "name_short": "Daffa",
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "project.html", context)


def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Daffa Akmal Mahadaya Pasaribu",
        "name_short": "Daffa",
        "form": form,
    }
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_project")

    context = {
        "name": "Daffa Akmal Mahadaya Pasaribu",
        "name_short": "Daffa",
        "form": form,
    }
    return render(request, "project_form.html", context)


@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_project")

    return redirect("main:show_project")


@login_required(login_url="/login/")
def toggle_star_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_project")


@login_required(login_url="/login/")
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")


@login_required(login_url="/login/")
def toggle_star_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        if request.user in education.starred_by.all():
            education.starred_by.remove(request.user)
        else:
            education.starred_by.add(request.user)

    return redirect("main:show_education")


def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


def get_project_json(request):
    title_query = request.GET.get("title", "").strip()
    project = Project.objects.prefetch_related("starred_by").all()

    if title_query:
        project = project.filter(title__icontains=title_query)

    data = []
    for pr in project:
        starred_users = pr.starred_by.all()
        is_starred = (
            request.user in starred_users if request.user.is_authenticated else False
        )
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append(
            {
                "pk": str(pr.id),
                "fields": {
                    "title": pr.title,
                    "description": pr.description,
                    "category": pr.get_category_display(),
                    "project_url": pr.project_url,
                    "star_count": starred_users.count(),
                    "is_starred": is_starred,
                    "starred_by_names": starred_by_names,
                },
            }
        )
    return JsonResponse(data, safe=False)


def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experience = Experience.objects.all()

    if title_query:
        experience = experience.filter(title__icontains=title_query)

    experience_json = serializers.serialize(
        "json", experience, use_natural_foreign_keys=True  # Tambahkan argumen ini
    )
    return HttpResponse(experience_json, content_type="application/json")


def update_experience(request, experience_id):

    if not (request.user.is_superuser or request.user.has_perm("main.change_project")):
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Daffa Akmal Mahadaya Pasaribu",
        "name_short": "Daffa",
        "form": form,
        "experience": experience,
    }
    return render(request, "experience_form.html", context)


def update_project(request, project_id):

    if not (request.user.is_superuser or request.user.has_perm("main.change_project")):
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project berhasil diperbarui!")
        return redirect("main:show_project")

    context = {
        "name": "Daffa Akmal Mahadaya Pasaribu",
        "name_short": "Daffa",
        "form": form,
        "project": project,
    }
    return render(request, "project_form.html", context)


def show_education(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Daffa Akmal Mahadaya Pasaribu",
        "name_short": "Daffa",
        "title_query": title_query,
        "form": EducationForm(),
    }
    return render(request, "education.html", context)


def create_education(request):
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Education baru berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Daffa Akmal Mahadaya Pasaribu",
        "name_short": "Daffa",
        "form": form,
    }
    return render(request, "education_form.html", context)


def update_education(request, education_id):

    if not (request.user.is_superuser or request.user.has_perm("main.change_project")):
        raise PermissionDenied

    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(request.POST or None, instance=education)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Education berhasil diperbarui!")
        return redirect("main:show_education")

    context = {
        "name": "Daffa Akmal Mahadaya Pasaribu",
        "name_short": "Daffa",
        "form": form,
        "education": education,
    }
    return render(request, "education_form.html", context)


def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Education berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")


def get_education_json(request):
    # title_query = request.GET.get("title", "").strip()
    # education = Education.objects.all()

    # if title_query:
    #     education = education.filter(title__icontains=title_query)

    # education_json = serializers.serialize(
    #     "json", education, use_natural_foreign_keys=True  # Tambahkan argumen ini
    # )
    # return HttpResponse(education_json, content_type="application/json")
    title_query = request.GET.get("title", "").strip()
    education = Education.objects.prefetch_related("starred_by").all()

    if title_query:
        education = education.filter(title__icontains=title_query)

    data = []
    for ed in education:
        starred_users = ed.starred_by.all()
        is_starred = (
            request.user in starred_users if request.user.is_authenticated else False
        )
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append(
            {
                "pk": str(ed.id),
                "fields": {
                    "title": ed.title,
                    "description": ed.description,
                    "level": ed.get_level_display(),
                    "star_count": starred_users.count(),
                    "is_starred": is_starred,
                    "started_at": ed.started_at,
                    "ended_at": ed.ended_at,
                    "starred_by_names": starred_by_names,
                },
            }
        )
    return JsonResponse(data, safe=False)


@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@require_POST
def create_education_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan education."},
            status=403,
        )

    form = EducationForm(request.POST)
    if form.is_valid():
        education = form.save()
        return JsonResponse(
            {"message": "Education berhasil ditambahkan.", "pk": str(education.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)
