from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from .models import PrestamoNotebook


class PrestamoNotebookCRUDTests(TestCase):
    def setUp(self):
        self.admin_group, _ = Group.objects.get_or_create(name="admin")
        self.normal_group, _ = Group.objects.get_or_create(name="normal")
        self.viewer_group, _ = Group.objects.get_or_create(name="viewer")

        self.admin = User.objects.create_user(
            username="test_admin",
            password="Test12345!",
        )
        self.admin.groups.add(self.admin_group)

        self.normal = User.objects.create_user(
            username="test_normal",
            password="Test12345!",
        )
        self.normal.groups.add(self.normal_group)

        self.viewer = User.objects.create_user(
            username="test_viewer",
            password="Test12345!",
        )
        self.viewer.groups.add(self.viewer_group)

    def crear_prestamo(self):
        return PrestamoNotebook.objects.create(
            nombre="Juan",
            edad=20,
            cupos_disponibles=2,
            estado=PrestamoNotebook.Estado.ACEPTADO,
            motivo="La persona cumple la edad requerida y hay notebooks disponibles.",
        )

    def test_crear_prestamo(self):
        self.client.force_login(self.normal)

        response = self.client.post(
            reverse("prestamo_crear"),
            {
                "nombre": "Ana",
                "edad": 20,
                "cupos_disponibles": 2,
            },
        )

        self.assertRedirects(response, reverse("prestamo_lista"))

        prestamo = PrestamoNotebook.objects.get(nombre="Ana")

        self.assertEqual(
            prestamo.estado,
            PrestamoNotebook.Estado.ACEPTADO,
        )

    def test_editar_recalcula_estado(self):
        prestamo = self.crear_prestamo()

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse("prestamo_editar", args=[prestamo.pk]),
            {
                "nombre": "Juan",
                "edad": 17,
                "cupos_disponibles": 2,
            },
        )

        self.assertRedirects(response, reverse("prestamo_lista"))

        prestamo.refresh_from_db()

        self.assertEqual(
            prestamo.estado,
            PrestamoNotebook.Estado.RECHAZADO,
        )
        self.assertEqual(
            prestamo.motivo,
            "La persona es menor de 18 años.",
        )

    def test_eliminar_es_borrado_logico(self):
        prestamo = self.crear_prestamo()

        self.client.force_login(self.admin)

        response = self.client.post(
            reverse("prestamo_eliminar", args=[prestamo.pk])
        )

        self.assertRedirects(response, reverse("prestamo_lista"))

        prestamo.refresh_from_db()

        self.assertTrue(prestamo.eliminado)
        self.assertIsNotNone(prestamo.fecha_eliminacion)

    def test_viewer_no_puede_crear(self):
        self.client.force_login(self.viewer)

        response = self.client.get(reverse("prestamo_crear"))

        self.assertEqual(response.status_code, 403)

    def test_normal_no_puede_editar(self):
        prestamo = self.crear_prestamo()

        self.client.force_login(self.normal)

        response = self.client.get(
            reverse("prestamo_editar", args=[prestamo.pk])
        )

        self.assertEqual(response.status_code, 403)

    def test_admin_puede_editar(self):
        prestamo = self.crear_prestamo()

        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("prestamo_editar", args=[prestamo.pk])
        )

        self.assertEqual(response.status_code, 200)
