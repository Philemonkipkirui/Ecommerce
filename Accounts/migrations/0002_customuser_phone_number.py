# Generated by Django 5.2 on 2025-04-11 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="phone_number",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
