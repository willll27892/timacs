# Generated by Django 2.2.7 on 2020-05-10 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_productrequest_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productrequest',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
