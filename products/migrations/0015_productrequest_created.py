# Generated by Django 2.2.7 on 2020-05-10 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20200510_0413'),
    ]

    operations = [
        migrations.AddField(
            model_name='productrequest',
            name='created',
            field=models.DateTimeField(null=True),
        ),
    ]
