# Generated by Django 3.2.7 on 2021-09-25 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='games',
            name='has_solo_entry',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='games',
            name='has_squad_entry',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='games',
            name='squad_entry_members',
            field=models.IntegerField(default=5),
        ),
    ]