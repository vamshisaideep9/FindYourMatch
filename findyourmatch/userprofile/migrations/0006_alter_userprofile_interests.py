# Generated by Django 5.1.7 on 2025-03-31 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_alter_userprofile_interests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='interests',
            field=models.ManyToManyField(blank=True, related_name='user_profiles', to='userprofile.interest'),
        ),
    ]
