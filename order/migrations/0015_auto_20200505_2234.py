# Generated by Django 2.2.7 on 2020-05-06 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_auto_20200505_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suborder',
            name='state',
            field=models.CharField(choices=[('sold', 'sold'), ('refunded', 'refunded'), ('available', 'available'), ('cancelled', 'cancelled')], default='processing', max_length=100),
        ),
    ]
