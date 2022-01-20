# Generated by Django 4.0.1 on 2022-01-20 14:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0004_alter_payments_payment_status"),
        ("main", "0009_games_registrations_closed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gamegroup",
            name="payment_id",
            field=models.ForeignKey(
                help_text="This is to be filled by computer",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="payments.payments",
            ),
        ),
    ]
