# Generated by Django 2.2.7 on 2020-05-05 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20200504_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='instock',
            field=models.IntegerField(null=True),
        ),
    ]
