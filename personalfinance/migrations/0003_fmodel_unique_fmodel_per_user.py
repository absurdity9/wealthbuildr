# Generated by Django 5.0.6 on 2024-06-25 21:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("personalfinance", "0002_alter_fmodel_created"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="fmodel",
            constraint=models.UniqueConstraint(
                fields=("user", "fmodel_name"), name="unique_fmodel_per_user"
            ),
        ),
    ]