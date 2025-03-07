from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active')  # Defina os campos que você quer exibir no admin
    search_fields = ('email', 'username')  # Campos que podem ser buscados
    list_filter = ('is_staff', 'is_active')  # Filtros no admin

admin.site.register(CustomUser, CustomUserAdmin)
