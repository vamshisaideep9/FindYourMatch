# Generated by Django 5.1.7 on 2025-04-05 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0006_alter_userprofile_interests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interest',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
