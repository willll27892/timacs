# Generated by Django 2.2.7 on 2020-03-29 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_cart_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='pdcount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
