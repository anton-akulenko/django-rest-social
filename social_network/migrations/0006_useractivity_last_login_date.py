# Generated by Django 5.0 on 2023-12-22 10:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("social_network", "0005_user_last_login_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="useractivity",
            name="last_login_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
