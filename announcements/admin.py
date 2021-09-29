from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_admin_listfilter_dropdown.filters import DropdownFilter
from .models import *


# Register your models here.
class GlobalAnnouncementsAdmin(admin.ModelAdmin):
    list_display = ('announcement_id', 'announncement_message',
                    'announncement_creation_date',)
    list_filter = (
        'announncement_creation_date',
    )
    search_fields = list_display + list_filter
    readonly_fields = ('announncement_creation_date', 'announcement_id')
    list_per_page = 20

    fieldsets = (
        (_('Id'), {'fields': ('announcement_id',)}),
        (_('Message'), {'fields': ('announncement_message',)}),
        (_('Creation'), {'fields': list_filter}),
    )
    class Media:
        js = ('js/richTextEditor.js',)

class GroupsAnnouncementsAdmin(admin.ModelAdmin):
    list_display = ('announcement_id', 'announncement_message',
                    'announncement_creation_date',)
    list_filter = (
        'announncement_creation_date',
    )
    search_fields = list_display + list_filter
    readonly_fields = ('announncement_creation_date', 'announcement_id')
    list_per_page = 20

    fieldsets = (
        (_('Id'), {'fields': ('announcement_id',)}),
        (_('Message'), {'fields': ('announncement_message',)}),
        (_('Groups'),{'fields': ('groups',)}),
        (_('Creation'), {'fields': list_filter}),
    )
    class Media:
        js = ('js/richTextEditor.js',)
    
class UsersAnnouncementsAdmin(admin.ModelAdmin):
    list_display = ('announcement_id', 'announncement_message',
                    'announncement_creation_date',)
    list_filter = (
        'announncement_creation_date',
    )
    search_fields = list_display + list_filter
    readonly_fields = ('announncement_creation_date', 'announcement_id')
    list_per_page = 20

    fieldsets = (
        (_('Id'), {'fields': ('announcement_id',)}),
        (_('Message'), {'fields': ('announncement_message',)}),
        (_('Users'),{'fields': ('users',)}),
        (_('Creation'), {'fields': list_filter}),
    )
    class Media:
        js = ('js/richTextEditor.js',)

    
admin.site.register(GlobalAnnouncements, GlobalAnnouncementsAdmin)
admin.site.register(GroupsAnnouncements, GroupsAnnouncementsAdmin)
admin.site.register(UsersAnnouncements, UsersAnnouncementsAdmin)
