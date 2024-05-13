from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib import admin
from .forms import UserCreationForm
from django.conf import settings


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    list_display = (
        "username",
        "is_staff",
        "is_superuser",
    )  # Added is_staff to match your User model
    list_filter = ("is_superuser",)

    # Define fieldsets for user detail view
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_superuser")},
        ),
    )

    # Define add_fieldsets for the create user form. Adjust as needed.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )

    search_fields = ("username",)
    ordering = ("username",)
    filter_horizontal = ()


# Don't forget to register the User model with the updated UserAdmin
admin.site.register(get_user_model(), UserAdmin)
