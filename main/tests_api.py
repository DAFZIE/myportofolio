import uuid

from django.contrib.auth.models import Group, Permission, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Education, Project


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", description="My website", category="project-small",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app", "category": "project-big",
            "project_url": "https://example.com/",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"project_url": "javascript:alert(1)"}, "project_url"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class EducationAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(username="owner", password="test-password")
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.editor = User.objects.create_user(username="editor")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.payload = {
            "title": "Universitas Indonesia", "description": "Ilmu Komputer",
            "level": "S1", "started_at": "2025-08-01T00:00:00Z", "ended_at": None,
        }
        self.education = Education.objects.create(**self.payload)
        self.list_url = reverse("api:education-list")
        self.detail_url = reverse("api:education-detail", args=[self.education.id])
        self.star_url = reverse("api:education-star", args=[self.education.id])

    def education_snapshot(self):
        return list(Education.objects.order_by("id").values())

    def test_public_read_search_and_safe_methods(self):
        response = self.client.get(self.list_url, {"title": "INDONESIA"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["id"], str(self.education.id))
        self.assertNotIn("email", response.data[0])
        self.assertEqual(self.client.get(self.list_url, {"title": "missing"}).data, [])
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)
        for method in (self.client.head, self.client.options):
            self.assertEqual(method(self.detail_url).status_code, 200)
        self.assertEqual(Education.objects.count(), 1)

    def test_owner_crud_and_validation(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Education.objects.filter(pk=response.data["id"]).exists())
        snapshot = self.education_snapshot()
        for changes, field in [
            ({"title": "<br>"}, "title"),
            ({"description": "<br>"}, "description"),
            ({"level": "unknown"}, "level"),
            ({"started_at": "invalid"}, "started_at"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, 400)
            self.assertIn(field, response.data)
            self.assertEqual(self.education_snapshot(), snapshot)
        self.assertEqual(self.client.put(self.detail_url, {"title": "Incomplete"}, format="json").status_code, 400)
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 200)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertFalse(Education.objects.filter(pk=self.education.id).exists())
        self.assertEqual(self.client.get(self.detail_url).status_code, 404)

    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.client.force_authenticate(self.editor)
        response = self.client.patch(self.detail_url, {"title": "<b>Updated</b>"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.education.refresh_from_db()
        self.assertEqual(self.education.title, "Updated")
        self.assertEqual(self.education.description, self.payload["description"])
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 200)
        snapshot = self.education_snapshot()
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.education_snapshot(), snapshot)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(self.education_snapshot(), snapshot)

    def test_existing_editor_permission_is_preserved(self):
        self.visitor.user_permissions.add(Permission.objects.get(codename="change_project"))
        self.client.force_authenticate(self.visitor)
        self.assertEqual(self.client.patch(self.detail_url, {"title": "Updated"}, format="json").status_code, 200)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)

    def test_guest_and_visitor_cannot_write(self):
        snapshot = self.education_snapshot()
        for user in (None, self.visitor):
            self.client.force_authenticate(user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.education_snapshot(), snapshot)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.education_snapshot(), snapshot)
            self.assertEqual(self.client.put(self.detail_url, {**self.payload, "title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.education_snapshot(), snapshot)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
            self.assertEqual(self.education_snapshot(), snapshot)

    def test_star_is_personal_and_read_only(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.assertEqual(self.education.starred_by.count(), 0)
        self.client.force_authenticate(self.visitor)
        self.assertEqual(self.client.get(self.star_url).status_code, 405)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(list(self.education.starred_by.values_list("pk", flat=True)), [self.visitor.pk])
        self.assertEqual(response.data["starred_by_names"], "visitor")
        self.client.force_authenticate(self.owner)
        response = self.client.get(self.detail_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.patch(self.detail_url, {
            "star_count": 99, "starred_by": [], "is_starred": True,
        }, format="json")
        self.assertEqual(response.data["star_count"], 1)
        self.assertFalse(response.data["is_starred"])
        self.client.force_authenticate(self.visitor)
        self.assertEqual(self.client.post(self.star_url).data["star_count"], 0)

    def test_session_csrf_on_portfolio_pages(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="visitor", password="test-password"))
        self.assertEqual(client.post(self.star_url).status_code, 403)
        self.assertEqual(self.education.starred_by.count(), 0)
        for page_name, star_url in [
            ("main:show_education", self.star_url),
            ("main:show_project", reverse("api:project-star", args=[Project.objects.create(
                title="Demo", description="Demo", category="project-small",
            ).id])),
        ]:
            client.cookies.pop("csrftoken", None)
            self.assertEqual(client.get(reverse(page_name)).status_code, 200)
            token = client.cookies["csrftoken"].value
            self.assertEqual(client.post(star_url, HTTP_X_CSRFTOKEN=token).status_code, 200)

    def test_session_owner_writes_require_csrf(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        snapshot = self.education_snapshot()
        for method, url, payload in [
            (client.post, self.list_url, self.payload),
            (client.patch, self.detail_url, {"title": "Changed"}),
            (client.delete, self.detail_url, {}),
        ]:
            self.assertEqual(method(url, payload, format="json").status_code, 403)
            self.assertEqual(self.education_snapshot(), snapshot)
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, "rest_framework")
        token = client.cookies["csrftoken"].value
        response = client.patch(self.detail_url, {"title": "Updated with CSRF"},
                                format="json", HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 200)
        self.education.refresh_from_db()
        self.assertEqual(self.education.title, "Updated with CSRF")

    def test_edit_page_uses_api_and_preserves_dates(self):
        self.client.force_login(self.editor)
        response = self.client.get(reverse("main:update_education", args=[self.education.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'data-api-url="{self.detail_url}"')
        self.assertContains(response, 'data-api-method="PATCH"')
        self.assertContains(response, 'value="2025-08-01T00:00"')
        self.assertContains(response, 'js/education_form.js')

    def test_legacy_views_follow_same_write_permissions(self):
        snapshot = self.education_snapshot()
        for user in (None, self.visitor, self.editor):
            self.client.logout()
            if user is not None:
                self.client.force_login(user)
            for name, args in [
                ("main:create_education", []),
                ("main:create_education_ajax", []),
                ("main:delete_education", [self.education.id]),
            ]:
                self.assertEqual(self.client.post(reverse(name, args=args), self.payload,
                                                 format="json").status_code, 403)
                self.assertEqual(self.education_snapshot(), snapshot)
            if user != self.editor:
                url = reverse("main:update_education", args=[self.education.id])
                self.assertEqual(self.client.post(url, {"title": "Changed"}).status_code, 403)
                self.assertEqual(self.education_snapshot(), snapshot)

