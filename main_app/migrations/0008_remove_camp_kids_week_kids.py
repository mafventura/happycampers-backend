# Generated by Django 4.2.10 on 2024-02-28 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_camp_kids'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camp',
            name='kids',
        ),
        migrations.AddField(
            model_name='week',
            name='kids',
            field=models.ManyToManyField(related_name='weeks', to='main_app.kid'),
        ),
    ]