# Generated by Django 2.2.7 on 2020-05-04 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20200503_0341'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='instock',
            field=models.IntegerField(null=True),
        ),
    ]
