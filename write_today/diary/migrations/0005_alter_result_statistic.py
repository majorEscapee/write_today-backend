# Generated by Django 5.0.3 on 2024-05-25 01:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diary", "0004_rename_achivement_achievement_remove_result_color_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="result",
            name="statistic",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="results",
                to="diary.statistic",
            ),
        ),
    ]
