# Generated by Django 4.2.10 on 2024-02-29 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_remove_camp_kids_week_kids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='week',
            name='kids',
            field=models.ManyToManyField(blank=True, related_name='weeks', to='main_app.kid'),
        ),
    ]