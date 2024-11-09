# Generated by Django 5.1.3 on 2024-11-08 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Voter",
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
                ("first_name", models.TextField()),
                ("last_name", models.TextField()),
                ("address_street_number", models.IntegerField()),
                ("address_street_name", models.TextField()),
                ("address_apt_number", models.IntegerField()),
                ("address_zip_code", models.IntegerField()),
                ("birth_date", models.DateField()),
                ("register_date", models.DateField()),
                ("party", models.CharField(max_length=1)),
                ("precinct", models.IntegerField()),
                ("v20state", models.BooleanField()),
                ("v21town", models.BooleanField()),
                ("v21primary", models.BooleanField()),
                ("v22general", models.BooleanField()),
                ("v23town", models.BooleanField()),
            ],
        ),
    ]
