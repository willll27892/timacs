# Generated by Django 2.2.7 on 2020-05-03 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_suborder_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suborder',
            name='reason',
            field=models.CharField(default='pending', max_length=200),
        ),
    ]
