# Generated by Django 5.1.7 on 2025-03-21 09:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userprofile", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="interest",
            name="category",
            field=models.ForeignKey(
                default=12,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="interests",
                to="userprofile.category",
            ),
        ),
    ]
