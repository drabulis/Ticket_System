from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'company', 'status', 'priority', 'created_by', 'assigned_to', 'created_at']
    list_filter = ['status', 'priority', 'company', 'created_at']
    search_fields = ['title', 'description', 'company__name']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['company', 'created_by', 'assigned_to']
    
    fieldsets = (
        ('Ticket Information', {
            'fields': ('title', 'description', 'company')
        }),
        ('Assignment', {
            'fields': ('created_by', 'assigned_to')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'resolved_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new ticket
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
