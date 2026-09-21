from django.forms import ModelForm, TextInput, Textarea, URLInput, DateTimeInput

from main.models import Project, Experience, Education


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "category",
            "project_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "category": "Kategori Proyek",
            "project_url": "URL Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Nama Proyekmu",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Deskripsi Proyekmu",
                    "rows": 3,
                }
            ),
            "category": TextInput(
                attrs={
                    "placeholder": "project-small, project-big",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/DAFZIE/myportofolio",
                }
            ),
        }


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Nama Pekerjaan",
            "description": "Deskripsi Pekerjaan",
            "category": "Kategori Pekerjaan",
            "thumbnail": "Thumbnail Pekerjaan",
            "started_at": "Tanggal Awal Pekerjaan",
            "ended_at": "Tanggal Selesai Pekerjaan",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Nama Pekerjaanmu",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Deskripsi Pekerjaanmu",
                    "rows": 3,
                }
            ),
            "category": TextInput(
                attrs={
                    "placeholder": "internship, research, volunteer, part-time, full-time, freelance",
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=19gdgESDiVMlbBQGohfIsP5wK8ts1y9hW&sz=w1000",
                }
            ),
            "started_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
            "ended_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
        }


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "title",
            "description",
            "level",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Nama Pendidikan",
            "description": "Deskripsi Pendidikan",
            "level": "Jenjang Pendidikan",
            "started_at": "Tanggal Mulai Pendidikan",
            "ended_at": "Tanggal Selesai Pendidikan",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Nama Sekolah/Universitasmu",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Deskripsi Jenjang Pendidikanmu",
                    "rows": 3,
                }
            ),
            "level": TextInput(
                attrs={
                    "placeholder": "SD, SMP, SMA, S1, S2, S3",
                }
            ),
            "started_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
            "ended_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
        }
