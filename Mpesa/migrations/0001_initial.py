# Generated by Django 5.2 on 2025-04-09 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Transaction",
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
                ("short_code", models.CharField(max_length=100)),
                ("msisdn", models.CharField(max_length=15)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("bill_ref_number", models.CharField(max_length=100)),
                ("transaction_id", models.CharField(max_length=255, unique=True)),
                ("status", models.CharField(default="Pending", max_length=100)),
            ],
        ),
    ]
