# Generated by Django 2.2.7 on 2020-03-25 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0007_auto_20200321_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='membership',
            field=models.CharField(choices=[('Per Sale', 'Pay per Sale'), ('Subscription', 'Subscription')], max_length=30, null=True),
        ),
    ]
