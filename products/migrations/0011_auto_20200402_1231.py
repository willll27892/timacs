# Generated by Django 2.2.7 on 2020-04-02 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20200402_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsize',
            name='sizeprice',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
