from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
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

    # API REST
    path("api/", include(router.urls)),

    # Autenticación JWT
    path("api/token/", TokenObtainPairView.as_view(), name="api_token"),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="api_token_refresh",
    ),
]
