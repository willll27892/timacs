# Generated by Django 2.2.7 on 2020-03-22 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0005_auto_20200318_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='membership',
            field=models.CharField(choices=[('Per product', 'Pay per product'), ('Subscription', 'Subscription')], max_length=30, null=True),
        ),
    ]
