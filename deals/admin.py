from django.contrib import admin
from .models import Deal


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['title', 'deal_type', 'get_discount_display', 'start_date', 'end_date', 'is_active', 'is_featured']
    list_filter = ['deal_type', 'is_active', 'is_featured', 'start_date']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'is_featured']
    filter_horizontal = ['products']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'deal_type')
        }),
        ('Discount Details', {
            'fields': ('discount_percentage', 'discount_amount')
        }),
        ('Products', {
            'fields': ('products',)
        }),
        ('Media', {
            'fields': ('banner_image',)
        }),
        ('Validity', {
            'fields': ('start_date', 'end_date', 'is_active', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
