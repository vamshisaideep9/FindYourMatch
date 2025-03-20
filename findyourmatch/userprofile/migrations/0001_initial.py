# Generated by Django 5.1.7 on 2025-03-20 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Interest",
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
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Language",
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
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="UserAccountSettings",
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
                (
                    "account_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Active", "Active"),
                            ("Paused", "Paused"),
                            ("Banned", "Banned"),
                        ],
                        max_length=30,
                        null=True,
                    ),
                ),
                ("is_verified", models.BooleanField(default=False)),
                ("last_seen", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="UserInteractions",
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
                ("is_online", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="UserLike",
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
                ("liked_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
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
                (
                    "display_name",
                    models.CharField(blank=True, max_length=30, null=True, unique=True),
                ),
                ("bio", models.TextField(blank=True)),
                (
                    "profile_picture",
                    models.ImageField(
                        blank=True, null=True, upload_to="profile_pictures/"
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Male", "Male"),
                            ("Female", "Female"),
                            ("Non-Binary", "Non binary"),
                            ("Other", "Other"),
                        ],
                        max_length=10,
                        null=True,
                    ),
                ),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                (
                    "height_unit",
                    models.CharField(
                        choices=[("cm", "Cm"), ("ft", "Feet")],
                        default="cm",
                        max_length=2,
                    ),
                ),
                (
                    "ethnicity",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Asian", "Asian"),
                            ("Black", "Black"),
                            ("Caucasian", "Caucasian"),
                            ("Hispanic", "Hispanic"),
                            ("Middle Eastern", "Middle eastern"),
                            ("Mixed", "Mixed"),
                            ("Other", "Other"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "religion",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Christianity", "Christianity"),
                            ("Islam", "Islam"),
                            ("Hinduism", "Hinduism"),
                            ("Buddhism", "Buddhism"),
                            ("Judaism", "Judaism"),
                            ("Atheist", "Atheist"),
                            ("Other", "Other"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "current_location",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "native_place",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "interested_in",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Male", "Male"),
                            ("Female", "Female"),
                            ("Non-Binary", "Non binary"),
                            ("Other", "Other"),
                        ],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "relationship_goals",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Casual Dating", "Casual"),
                            ("Serious Relationship", "Serious"),
                            ("Marriage", "Marriage"),
                            ("Friendship", "Friends"),
                            ("Not Sure", "Not sure"),
                        ],
                        max_length=30,
                        null=True,
                    ),
                ),
                ("age_preference_min", models.IntegerField(default=18)),
                ("age_preference_max", models.IntegerField(default=99)),
                ("distance_preference", models.IntegerField(default=50)),
                ("hobbies", models.TextField(blank=True)),
                ("education", models.CharField(blank=True, max_length=100, null=True)),
                ("occupation", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "smoking",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Never", "Never"),
                            ("Regularly", "Regularly"),
                            ("Socially", "Socially"),
                            ("Trying to Quit", "Trying to quit"),
                        ],
                        max_length=30,
                        null=True,
                    ),
                ),
                (
                    "drinking",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Never", "Never"),
                            ("Regularly", "Regularly"),
                            ("Socially", "Socially"),
                            ("Trying to Quit", "Trying to quit"),
                        ],
                        max_length=30,
                        null=True,
                    ),
                ),
                (
                    "pets",
                    models.CharField(
                        blank=True,
                        choices=[("Dogs", "Dog"), ("Cats", "Cat"), ("Other", "Other")],
                        max_length=30,
                        null=True,
                    ),
                ),
            ],
        ),
    ]
