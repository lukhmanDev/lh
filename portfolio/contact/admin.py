from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    list_editable = ('is_read',)
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

    @admin.action(description='Mark selected submissions as read')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description='Mark selected submissions as unread')
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
