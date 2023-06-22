from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("admin_volt.urls")),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("articles/", include("articles.urls")),
    path("api/ai_process/", include("ai_process.urls")),
]
