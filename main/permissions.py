from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrReadOnly(BasePermission):
    message = "Only the portfolio owner can change projects."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
        )


def can_edit_education(user):
    # Earlier assignments used change_project as the Editor permission.
    return user.is_authenticated and (
        user.is_superuser
        or user.has_perm("main.change_project")
        or user.has_perm("main.change_education")
        or user.groups.filter(name="Editor").exists()
    )


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return (
            request.method in ("PUT", "PATCH")
            and can_edit_education(request.user)
        )
