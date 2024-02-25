from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from traders.models import Trader


@admin.action(description='Clear debt in selected traders')
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt=None)


@admin.register(Trader)
class TraderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'email', 'country', 'city', 'vendor_link', 'type', 'level', 'debt', ]
    list_display_links = ['title']
    fields = [
        'title',
        ('type', 'level'),
        ('email', 'country', 'city', 'street', 'house'),
        'products',
        ('vendor', 'debt'),
        'created_at',
    ]
    readonly_fields = ['created_at', 'level', ]
    list_filter = ['city']
    actions = [clear_debt]

    def vendor_link(self, obj):
        vendor_id = Trader.objects.filter(title=obj.vendor)
        if vendor_id:
            link = reverse("admin:traders_trader_change", args=[obj.vendor_id])
            return format_html(u'<a href="%s">%s</a>' % (link, obj.vendor))
        return '-'

    vendor_link.short_description = 'Поставщик'
