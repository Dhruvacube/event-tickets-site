from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('payments/', include('payments.urls')),
    path('', home,name="home"),
    path('make_groups/', group_make, name="make_groups"),
    path('about_game/<int:game_id>', view_games, name="about_game"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
