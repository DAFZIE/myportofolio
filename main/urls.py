from django.urls import path

from main.views import (
    show_main,
    show_experience,
    show_project,
    create_project,
    get_project_json,
    delete_project,
    create_experience,
    get_experience_json,
    delete_experience,
    update_experience,
    update_project,
    show_education,
    create_education,
    update_education,
    get_education_json,
    delete_education,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("project/", show_project, name="show_project"),
    path("education/", show_education, name="show_education"),
    path("project/add/", create_project, name="create_project"),
    path("project/<uuid:project_id>/edit/", update_project, name="update_project"),
    path("experience/add/", create_experience, name="create_experience"),
    path(
        "experience/<uuid:experience_id>/edit/",
        update_experience,
        name="update_experience",
    ),
    path("education/add/", create_education, name="create_education"),
    path(
        "education/<uuid:education_id>/edit/", update_education, name="update_education"
    ),
    path("api/project/", get_project_json, name="get_project_json"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    path("api/education/", get_education_json, name="get_education_json"),
    path("project/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path(
        "projects/<uuid:experience_id>/delete/",
        delete_experience,
        name="delete_experience",
    ),
    path(
        "education/<uuid:education_id>/delete/",
        delete_education,
        name="delete_education",
    ),
]
