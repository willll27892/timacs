# Generated by Django 2.2.7 on 2020-04-21 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0021_activity_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='display',
            new_name='incart',
        ),
    ]