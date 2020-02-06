# Generated by Django 2.2.10 on 2020-02-06 10:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("protector", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="resource",
            name="author",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="resource",
            name="url",
            field=models.URLField(
                blank=True,
                help_text="Type URL Address that you want to protect",
                verbose_name="URL Address",
            ),
        ),
    ]