# Generated by Django 5.0.3 on 2024-05-24 04:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diary", "0002_alter_diary_created_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="diary",
            name="created_date",
            field=models.DateField(unique=True),
        ),
    ]
