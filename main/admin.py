from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_admin_listfilter_dropdown.filters import ChoiceDropdownFilter


# Register your models here.
class GamesAdmin(admin.ModelAdmin):
    list_display = ('name', 'platform',
                    'solo_entry', 'squad_entry')
    list_filter = (
        ('platform', ChoiceDropdownFilter),
    )
    search_fields = list_display + list_filter + ('image_url',)
    readonly_fields = ('view_image', )
    list_per_page = 15

    fieldsets = (
        (_('Name'), {'fields': ('name',)}),
        (_('Description'), {'fields': ('short_description', 'long_description')}),
        (_('Image'), {'fields': ('image_url',)+readonly_fields}),
        (_('pPlatform'), {'fields': ('platform', )}),
        (_('Entry Price'), {'fields': ('solo_entry', 'squad_entry',)})
    )