from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User, Fridge


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    readonly_fields = ("last_login",)
    list_display = [
        "username",
        "age",
        "gender",
        "pk",
        "email",
        "is_admin",
        "login_type",
    ]
    list_filter = [
        "is_admin",
    ]
    fieldsets = [
        (
            "Profile",
            {
                "fields": (
                    "email",
                    "password",
                    "avatar",
                    "username",
                    "age",
                    "gender",
                    "followings",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_admin",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important Dates",
            {
                "fields": ("last_login",),
                "classes": ("collapse",),
            },
        ),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email", "username"]
    ordering = ["email"]


@admin.register(Fridge)
class FridgeAdmin(admin.ModelAdmin):
    pass
