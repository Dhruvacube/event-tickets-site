from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from main.models import Games


class StaticViewSitemap(Sitemap):
    changefreq = "never"

    @staticmethod
    def priority(item):
        return 1.0 if item[0] in ("H", "s", "R") else 0.80

    def items(self):
        games, l = Games.objects.values("id").iterator(), []
        for i in games:
            l.extend([f'about_game/{game_id["id"]}' for game_id in games])
        return ["home", "signin", "signout", "signup"] + l

    def location(self, item):
        if item in ("home", "signin", "signout", "signup"):
            return reverse(item)
        else:
            return reverse(item.split("/")[0], args=[item.split("/")[-1]])
