from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(TabDependencia)

admin.site.register(TabDescgrupo)

admin.site.register(TabDescproyec)

admin.site.register(TabDescreunion)

admin.site.register(TabEstatus)

admin.site.register(TabGrupo)

admin.site.register(TabMiembro)

admin.site.register(TabMconsejo)

admin.site.register(TabProyecto)

admin.site.register(TabReuniong)

admin.site.register(TabTiporeunion)

admin.site.register(TabTipodependencia)

admin.site.register(TabTipousuario)
