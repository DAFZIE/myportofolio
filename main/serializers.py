from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Education, Project


class PortfolioItemSerializer(serializers.ModelSerializer):
    """Shared text validation and public star metadata for portfolio items."""
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Description cannot be empty.")
        return value

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class ProjectSerializer(PortfolioItemSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "category", "project_url",
            "category_display", "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]


class EducationSerializer(PortfolioItemSerializer):
    class Meta:
        model = Education
        fields = [
            "id", "title", "description", "level", "started_at", "ended_at",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]
