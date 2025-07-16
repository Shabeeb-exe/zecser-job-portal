from django.contrib import admin
from django.shortcuts import redirect
from django.contrib.auth.admin import UserAdmin
from .models import Job, User, JobseekerProfile, EmployerProfile
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'full_name', 'role', 'is_staff', 'is_active', 'is_verified', 'verification_status')
    list_filter = ('role', 'is_staff', 'is_active', 'is_verified')
    search_fields = ('email', 'full_name')
    ordering = ('full_name',)
    actions = ['verify_users', 'unverify_users']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone_number')}),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'is_verified', 
                      'verification_token', 'verification_token_expires',
                      'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'role', 'is_staff', 'is_active', 'is_verified'),
        }),
    )
    
    readonly_fields = ('verification_token', 'verification_token_expires')
    
    def verification_status(self, obj):
        if obj.is_verified:
            return format_html('<span style="color: green;">✓ Verified</span>')
        elif obj.verification_token_expires and obj.verification_token_expires < timezone.now():
            return format_html('<span style="color: red;">✗ Token Expired</span>')
        else:
            return format_html(
                '<a class="button" href="{}">Send Verification</a>',
                reverse('admin:send_verification', args=[obj.pk])
            )
    verification_status.short_description = 'Verification Status'
    
    def verify_users(self, request, queryset):
        queryset.update(is_verified=True, verification_token=None)
        self.message_user(request, f"Successfully verified {queryset.count()} users.")
    verify_users.short_description = "Mark selected users as verified"
    
    def unverify_users(self, request, queryset):
        queryset.update(is_verified=False)
        self.message_user(request, f"Successfully unverified {queryset.count()} users.")
    unverify_users.short_description = "Mark selected users as unverified"
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/send-verification/',
                 self.admin_site.admin_view(self.send_verification),
                 name='send_verification'),
        ]
        return custom_urls + urls
    
    def send_verification(self, request, user_id):
        from .utils import send_verification_email
        user = User.objects.get(pk=user_id)
        send_verification_email(user)
        self.message_user(request, "Verification email sent successfully.")
        return redirect('..')

admin.site.register(User, CustomUserAdmin)
@admin.register(JobseekerProfile)
class JobseekerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_available', 'receive_job_alerts', 'alert_frequency')
    list_filter = ('is_available', 'receive_job_alerts', 'alert_frequency')
    search_fields = ('user__email', 'user__full_name', 'skills')
    raw_id_fields = ('user',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'company_size', 'industry')
    list_filter = ('company_size', 'industry')
    search_fields = ('company_name', 'user__email', 'user__full_name')
    raw_id_fields = ('user',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'location', 'job_type', 'is_active')
    list_filter = ('job_type', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'employer__company_name')
    raw_id_fields = ('employer',)