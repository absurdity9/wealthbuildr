# Generated by Django 5.0.6 on 2024-08-08 17:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="FModel",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("fmodel_name", models.CharField(max_length=100)),
                ("created", models.DateField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Expense",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("expense_name", models.CharField(max_length=100)),
                ("value", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "fmodel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="personalfinance.fmodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Asset",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("asset_name", models.CharField(max_length=100)),
                ("yield_rate", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "principle_amount",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "fmodel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="personalfinance.fmodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Income",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("income_name", models.CharField(max_length=100)),
                ("value", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "fmodel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="personalfinance.fmodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PublishedPage",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("page_name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=100, unique=True)),
                ("is_public", models.BooleanField(default=False)),
                ("published_date", models.DateTimeField(auto_now_add=True)),
                (
                    "fmodel",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="personalfinance.fmodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Userprofile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("age", models.IntegerField()),
                ("job", models.CharField(max_length=100)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="fmodel",
            constraint=models.UniqueConstraint(
                fields=("user", "fmodel_name"), name="unique_fmodel_per_user"
            ),
        ),
    ]
