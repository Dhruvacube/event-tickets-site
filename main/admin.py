from django.contrib import admin
from django.utils.translation import gettext_lazy as _
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
    
admin.site.register(Games, GamesAdmin)