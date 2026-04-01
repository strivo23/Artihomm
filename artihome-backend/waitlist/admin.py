from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import WaitlistEntry

@admin.register(WaitlistEntry)
class WaitlistEntryAdmin(admin.ModelAdmin):
    list_display    = ('get_email', 'product', 'name', 'phone', 'city', 'is_pledge', 'created_at')
    list_filter     = ('is_pledge', 'product__category', 'city', 'product')
    search_fields   = ('user__email', 'name', 'phone', 'product__name', 'city')
    readonly_fields = ('created_at', 'user')
    ordering        = ('-created_at',)
    date_hierarchy  = 'created_at'
    actions         = ['export_as_csv']

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'product')

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="artihome_waitlist.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Date', 'Name', 'Email', 'Phone', 'City',
            'Product', 'Category', 'Price (Rs.)', 'Requirements', 'Pledge'
        ])
        for entry in queryset.select_related('user', 'product'):
            # Fallback handling for missing attributes during transition
            writer.writerow([
                entry.created_at.strftime('%Y-%m-%d %H:%M') if hasattr(entry, 'created_at') else '',
                getattr(entry, 'name', ''),
                entry.user.email if hasattr(entry, 'user') and entry.user else '',
                getattr(entry, 'phone', ''),
                getattr(entry, 'city', ''),
                entry.product.name if hasattr(entry, 'product') and entry.product else '',
                getattr(entry.product, 'category', ''),
                getattr(entry.product, 'ah_price', getattr(entry.product, 'estimated_price', 0)) if hasattr(entry, 'product') else 0,
                getattr(entry, 'requirements', ''),
                'Yes' if getattr(entry, 'is_pledge', False) else 'No',
            ])
        return response
    export_as_csv.short_description = 'Export selected entries to CSV'
