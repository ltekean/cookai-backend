from django.contrib import admin
from django.urls import path, include
from .views import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health_check"),
    path("users/", include("users.urls")),
    path("articles/", include("articles.urls")),
    path("ai_process/", include("ai_process.urls")),
]
