import os
import secrets
import string
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from payments.models import *


def generate_unique_id():
    return "".join(
        secrets.choice(string.ascii_letters + string.digits +
                       str(secrets.randbits(7))) for i in range(7)).upper()


def format_list(list_images: list):
    list_images.remove("sponsers")
    return list_images


# Create your models here.
class Games(models.Model):
    game_unique_id = models.CharField(
        default=generate_unique_id,
        help_text=_("The Games ID by which the system refers"),
        max_length=250,
        unique=True,
    )
    name = models.CharField(max_length=200,
                            help_text=_("The name of the game"))
    short_description = models.TextField(
        help_text=_(
            "About this short event, better keep it in between 100 characters"
        ),
        validators=[MinLengthValidator(13),
                    MaxLengthValidator(200)],
    )
    long_description = models.TextField(help_text=_("Here explain everything"))
    image_url = models.CharField(help_text=_("Url of the game image"),
                                 max_length=250)
    platform = models.CharField(
        max_length=11,
        choices=(("a", "ALL"), ("m", "Mobile"), ("p", "PC"), ("ps",
                                                              "Play Station")),
        default="A",
    )

    has_solo_entry = models.BooleanField(default=True)
    solo_entry = models.IntegerField(help_text="Enter the Solo entry price",
                                     default=0)

    has_squad_entry = models.BooleanField(default=True)
    squad_entry = models.IntegerField(help_text="Enter the Sqaud entry price",
                                      default=0)
    squad_entry_members = models.IntegerField(default=5)
    registrations_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image_url.startswith("/"):
            self.image_url = self.image_url[1:]
        if self.image_url.endswith("/"):
            self.image_url = self.image_url[:-1]
        return super().save(*args, **kwargs)

    def view_image(self):
        if self.image_url:
            return mark_safe(
                f'<img loading="lazy" src="{settings.STATIC_URL}{self.image_url}" width="50%" height="50%" />'
            )
        return "None"

    @staticmethod
    def static_images_list():
        file_path = settings.BASE_DIR / os.path.join("main", "static",
                                                     "images")
        html_string = "".join([
            f" <li><a href='{settings.STATIC_URL}images/{i.strip(' ')}' target='_blank'>images/{i.strip(' ')}</a></li>"
            for i in format_list(os.listdir(file_path))
        ])
        return mark_safe(f"<ol>{html_string}</ol>")

    class Meta:
        verbose_name_plural = _("Games")


class GameGroup(models.Model):
    group_unique_id = models.UUIDField(default=uuid.uuid4)
    group_name = models.CharField(max_length=250,
                                  unique=True,
                                  blank=True,
                                  null=True)
    solo_or_squad = models.CharField(default="sq",
                                     choices=(("sq", "SQUAD"), ("so", "SOLO")),
                                     max_length=15)
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    payment_id = models.ForeignKey(
        Payments,
        on_delete=models.CASCADE,
        help_text=_("This is to be filled by computer"),
        null=True,
    )

    def __str__(self):
        return str(self.group_name)

    def payer_details(self):
        user = (get_user_model().objects.filter(
            orders__order_id=self.payment_id.order_id).values(
                "first_name", "last_name", "university_name", "phone",
                "email").get())
        return f"Name: {user['first_name']} {user['last_name']}\n University Name: {user['university_name']} \n Phone: {user['phone']} \n Email: {user['email']}"

    def save(self, *args, **kwargs):
        if self._state.adding and self.group_name in ("", " ", False, None):
            if self.solo_or_squad == "so":
                self.group_name = f"Solo {str(generate_unique_id()).upper()}"
            else:
                self.group_name = f"Group {str(generate_unique_id()).upper()}"
        return super().save(*args, **kwargs)


class Sponser(models.Model):
    name = models.CharField(max_length=250, unique=True)
    website = models.URLField()
    image = models.CharField(max_length=250)

    def __str__(self):
        return str(self.name)

    def view_image(self):
        if self.image:
            return mark_safe(
                f'<img loading="lazy" src="{settings.STATIC_URL}{self.image}" width="50%" height="50%" />'
            )
        return "None"

    @staticmethod
    def static_images_list():
        file_path = settings.BASE_DIR / os.path.join("main", "static",
                                                     "images", "sponsers")
        html_string = "".join([
            f" <li><a href='{settings.STATIC_URL}images/sponsers/{i.strip(' ')}' target='_blank'>images/sponsers/{i.strip(' ')}</a></li>"
            for i in os.listdir(file_path)
        ])
        return mark_safe(f"<ol>{html_string}</ol>")
