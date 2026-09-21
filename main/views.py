from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.models import Experience
from main.models import Project
from main.forms import ProjectForm, ExperienceForm


def show_main(request):
    context = {
        "name": "Daffa Akmal Mahadaya Pasaribu",
        "name_short": "Daffa",
        "npm": "2506584451",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Just another furry that studies in compsci "
            "and is trying to live his life to the fullest."
        ),
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
    json_response = get_project_json(request)

    project = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    project = [project.object for project in project]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Daffa Akmal Mahadaya Pasaribu",
        "name_short": "Daffa",
        "project_list": project,
        "title_query": title_query,
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


def create_project(request):
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


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_project")

    return redirect("main:show_project")


def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


def get_project_json(request):
    title_query = request.GET.get("title", "").strip()
    project = Project.objects.all()

    if title_query:
        project = project.filter(title__icontains=title_query)

    project_json = serializers.serialize("json", project)
    return HttpResponse(project_json, content_type="application/json")


def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experience = Experience.objects.all()

    if title_query:
        experience = experience.filter(title__icontains=title_query)

    experience_json = serializers.serialize("json", experience)
    return HttpResponse(experience_json, content_type="application/json")


# def show_project(request):
#     context = {
#         "name": "Daffa Akmal Mahadaya Pasaribu",
#         "name_short": "Daffa",
#         "project_list": Project.objects.all(),
#     }
#     return render(request, "project.html", context)
