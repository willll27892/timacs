# Generated by Django 2.2.7 on 2020-05-13 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20200510_0529'),
    ]

    operations = [
        migrations.AddField(
            model_name='tracker',
            name='state',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
