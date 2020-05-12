# Generated by Django 2.2.7 on 2020-05-03 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_orderstate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='orderstate',
            field=models.CharField(choices=[('Sold', 'Sold'), ('Refunded', 'Refunded'), ('available', 'available'), ('cancelled', 'cancelled')], default='available', max_length=200),
        ),
    ]
