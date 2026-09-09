from django.shortcuts import render

from main.models import Experience


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
    context = {
        "name": "Daffa Akmal Mahadaya Pasaribu",
        "name_short": "Daffa",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)
