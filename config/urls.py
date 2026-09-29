from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from core.api_views import PrestamoNotebookViewSet


router = DefaultRouter()
router.register(
    r"prestamos",
    PrestamoNotebookViewSet,
    basename="prestamo",
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("cuentas/", include("django.contrib.auth.urls")),
    path("", include("core.urls")),
    path("api/", include(router.urls)),
    path("api/token/", obtain_auth_token, name="api_token"),
]