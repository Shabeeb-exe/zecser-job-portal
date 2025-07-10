from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Job, User, JobseekerProfile, EmployerProfile

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'full_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email', 'full_name')
    ordering = ('full_name',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone_number')}),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'is_verified', 
                      'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'role', 'is_staff', 'is_active'),
        }),
    )
   
admin.site.register(User, CustomUserAdmin)
admin.site.register(JobseekerProfile)
admin.site.register(EmployerProfile)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'location', 'job_type', 'is_active')
    list_filter = ('job_type', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'employer__company_name')
    raw_id_fields = ('employer',)