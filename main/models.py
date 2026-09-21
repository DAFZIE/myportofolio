import uuid
from django.db import models


class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ("internship", "Internship"),
        ("research", "Research"),
        ("volunteer", "Volunteer"),
        ("part-time", "Part-Time"),
        ("full-time", "Full-Time"),
        ("freelance", "Freelance"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None


class Project(models.Model):
    PROJECT_CHOICES = [
        ("project-small", "Small Project"),
        ("project-big", "Big Project"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=PROJECT_CHOICES)
    project_url = models.URLField(blank=True)

    def __str__(self):
        return self.title


class Education(models.Model):
    EDUCATION_CHOICES = [
        ("SD", "SD"),
        ("SMP", "SMP"),
        ("SMA", "SMA"),
        ("S1", "S1"),
        ("S2", "S2"),
        ("S3", "S3"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    level = models.CharField(max_length=10, choices=EDUCATION_CHOICES)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.level})"

    @property
    def is_ongoing(self):
        return self.ended_at is None
