# Generated by Django 5.1.3 on 2024-11-19 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="phone_number",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="trip",
            name="destination",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="trip",
            name="end_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="trip",
            name="start_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]