# Generated by Django 2.2.7 on 2020-05-07 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0021_auto_20200506_1153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderstatus',
            old_name='commets',
            new_name='comments',
        ),
    ]