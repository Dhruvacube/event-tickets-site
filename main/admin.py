from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import Group
from django_admin_listfilter_dropdown.filters import DropdownFilter
from .models import *


# Register your models here.
class GamesAdmin(admin.ModelAdmin):
    list_display = ('name', 'platform',
                    'solo_entry', 'squad_entry')
    list_filter = (
        'platform',
    )
    search_fields = list_display + list_filter + ('image_url',)
    readonly_fields = ('view_image', )
    list_per_page = 15

    fieldsets = (
        (_('Name'), {'fields': ('name',)}),
        (_('Description'), {'fields': ('short_description', 'long_description')}),
        (_('Image'), {'fields': ('image_url',)+readonly_fields}),
        (_('Platform'), {'fields': ('platform', )}),
        (_('Solo Entry'), {'fields': ('has_solo_entry', 'solo_entry')}),
        (_('Squad Entry'), {'fields': ('has_squad_entry', 'squad_entry', 'squad_entry_members')})
    )
    class Media:
        js = ('js/richTextEditor.js',)

class GameGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'group_unique_id',
                    'solo_or_squad', 'game','payment_id')
    list_filter = (
        'solo_or_squad', 'game'
    )
    search_fields = list_display + list_filter
    list_per_page = 30

    fieldsets = (
        (_('Name'), {'fields': ('group_name', 'group_unique_id')}),
        (_('Mode'), {'fields': ('solo_or_squad',)}),
        (_('Game'), {'fields': ('game',)}),
        (_('Users'), {'fields': ('users', )}),
        (_('Payment ID'), {'fields': ('payment_id',)}),
    )
    
admin.site.register(Games, GamesAdmin)
admin.site.register(GameGroup, GameGroupAdmin)
admin.site.unregister(Group)

admin.site.site_header = admin.site.site_title = 'Tanzanite Gaming League 2.0'