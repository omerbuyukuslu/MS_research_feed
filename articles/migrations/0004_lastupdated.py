# Generated by Django 5.1.3 on 2024-12-14 22:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0003_alter_article_published_date_alter_article_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="LastUpdated",
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
                ("timestamp", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
