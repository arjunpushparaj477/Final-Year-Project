from django.contrib import admin
from .models import Zone, Cell

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone_leader', 'created_at')
    search_fields = ('name', 'zone_leader__username')
    list_filter = ('created_at',)

@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone', 'cell_leader', 'created_at')
    search_fields = ('name', 'zone__name', 'cell_leader__username')
    list_filter = ('zone', 'created_at')
