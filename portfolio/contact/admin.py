from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status_badge', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        ('Sender Information', {
            'fields': ('name', 'email')
        }),
        ('Inquiry Content', {
            'fields': ('subject', 'message')
        }),
        ('Review Status & Timestamp', {
            'fields': ('is_read', 'created_at')
        }),
    )

    actions = ['mark_as_read', 'mark_as_unread']

    @display(
        description='Status',
        label={
            'Read': 'success',
            'Unread': 'warning',
        }
    )
    def status_badge(self, obj: ContactMessage) -> str:
        return 'Read' if obj.is_read else 'Unread'

    @admin.action(description='Mark selected submissions as read')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description='Mark selected submissions as unread')
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
