# Generated by Django 2.2.7 on 2020-05-13 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0004_sellerid_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='state',
            field=models.CharField(max_length=200, null=True),
        ),
    ]