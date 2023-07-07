from django.contrib import admin
from django.urls import path, include


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("articles/", include("articles.urls")),
    path("ai_process/", include("ai_process.urls")),
    path("debug/", trigger_error),
]
