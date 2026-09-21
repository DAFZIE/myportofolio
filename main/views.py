from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.models import Experience, Project, Education
from main.forms import ProjectForm, ExperienceForm, EducationForm


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


def update_experience(request, experience_id):
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
    json_response = get_education_json(request)

    education = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    education = [education.object for education in education]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Daffa Akmal Mahadaya Pasaribu",
        "name_short": "Daffa",
        "education_list": education,
        "title_query": title_query,
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
    title_query = request.GET.get("title", "").strip()
    education = Education.objects.all()

    if title_query:
        education = education.filter(title__icontains=title_query)

    education_json = serializers.serialize("json", education)
    return HttpResponse(education_json, content_type="application/json")


# def show_project(request):
#     context = {
#         "name": "Daffa Akmal Mahadaya Pasaribu",
#         "name_short": "Daffa",
#         "project_list": Project.objects.all(),
#     }
#     return render(request, "project.html", context)
