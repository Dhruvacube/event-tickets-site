import uuid

from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from main.models import *


class GlobalAnnouncements(models.Model):
    announcement_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    announcement_heading = models.CharField(max_length=250,
                                            default="New Announcement Here")
    announncement_message = models.TextField(
        _("The announcement that you want to give globally"))
    publish = models.BooleanField(default=True)
    announncement_creation_date = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.announcement_id)

    class Meta:
        verbose_name_plural = "Global Announcements"
        ordering = ("-announncement_creation_date", )


class GroupsAnnouncements(models.Model):
    announcement_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    announcement_heading = models.CharField(max_length=250,
                                            default="New Announcement Here")
    announncement_message = models.TextField(
        _("The announcement that you want to give Group Wise"))
    groups = models.ManyToManyField(GameGroup)
    publish = models.BooleanField(default=True)
    announncement_creation_date = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.announcement_id)

    class Meta:
        verbose_name_plural = "Groups Announcements"
        ordering = ("-announncement_creation_date", )


class UsersAnnouncements(models.Model):
    announcement_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    announcement_heading = models.CharField(max_length=250,
                                            default="New Announcement Here")
    announncement_message = models.TextField(
        _("The announcement that you want to give per or user wise"))
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    publish = models.BooleanField(
        default=True,
        help_text=_("Check this when you want to publish this announcement"),
    )
    announncement_creation_date = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.announcement_id)

    class Meta:
        verbose_name_plural = "User Announcements"
        ordering = ("-announncement_creation_date", )
