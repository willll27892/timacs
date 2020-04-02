# Generated by Django 2.2.7 on 2020-04-02 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_product_availableseizes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='pdcolor',
        ),
        migrations.AddField(
            model_name='product',
            name='pdcolor',
            field=models.ManyToManyField(blank=True, null=True, related_name='_product_pdcolor_+', to='products.Product'),
        ),
    ]