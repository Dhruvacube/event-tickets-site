from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from announcements.views import *
from main.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("payments/", include("payments.urls")),
    path("", home, name="home"),
    path("make_groups/", group_make, name="make_groups"),
    path("about_game/<int:game_id>", view_games, name="about_game"),
    path("announcements/", view_annoucements, name="all_anouncements"),
    path(
        "announcements/<uuid:announcement_id>",
        view_annoucements_full,
        name="announcement_detail",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
