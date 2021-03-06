from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import RedirectView

from announcements.views import *
from main.views import *

from .sitemaps import StaticViewSitemap

sitemaps = {"static": StaticViewSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("accounts.urls")),
    path("accounts/", include("accounts.urls")),
    path("payments/", include("payments.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="Sitemap"),
    path("", home, name="home"),
    path("make_groups/", group_make, name="make_groups"),
    path("about_game/<int:game_id>", view_games, name="about_game"),
    path("announcements/", view_annoucements, name="all_anouncements"),
    path(
        "announcements/<uuid:announcement_id>",
        view_annoucements_full,
        name="announcement_detail",
    ),
    path(
        "privacy_policy/",
        RedirectView.as_view(
            url="https://github.com/Tanzanite-lpu/tgl-2.0/wiki/Privacy-Policy"
        ),
        name="privacy_policy",
    ),
    path(
        "cookie_policy/",
        RedirectView.as_view(
            url="https://github.com/Tanzanite-lpu/tgl-2.0/wiki/Cookie-Policy"),
        name="cookie_policy",
    ),
    path(
        "tos/",
        RedirectView.as_view(
            url="https://github.com/Tanzanite-lpu/tgl-2.0/wiki/Terms-&-Conditions"
        ),
        name="tos",
    ),
    path(
        "refunds/",
        RedirectView.as_view(
            url="https://github.com/Tanzanite-lpu/tgl-2.0/wiki/Cancellation--&-Refund-Policy"
        ),
        name="refunds",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
