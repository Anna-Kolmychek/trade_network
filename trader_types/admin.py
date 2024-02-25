from django.contrib import admin

from trader_types.models import TraderTypes


@admin.register(TraderTypes)
class TraderTypesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title',)
    list_display_links = ['title']
