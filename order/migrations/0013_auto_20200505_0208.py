# Generated by Django 2.2.7 on 2020-05-05 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_suborder_orderinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderstatus',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
    ]
