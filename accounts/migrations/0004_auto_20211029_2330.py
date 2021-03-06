# Generated by Django 3.2.8 on 2021-10-29 18:00

import django.core.validators
from django.db import migrations, models

import accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_alter_user_referral_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.CharField(
                help_text="It should be +91 67xxx",
                max_length=15,
                validators=[
                    django.core.validators.MinLengthValidator(13),
                    accounts.models.validate_phone,
                ],
                verbose_name="phone",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="registration_no",
            field=models.CharField(
                blank=True,
                help_text="Your college issued ID (Optional)",
                max_length=250,
                null=True,
                validators=[django.core.validators.MinLengthValidator(3)],
                verbose_name="Registration No",
            ),
        ),
    ]
