# Generated by Django 5.0.3 on 2024-05-26 17:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("diary", "0007_remove_achievement_requirement"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="collection",
            name="end_date",
        ),
    ]
