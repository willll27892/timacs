# Generated by Django 2.2.7 on 2020-04-05 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_productcolor_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='costprocessing',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.ProductColor'),
        ),
        migrations.AddField(
            model_name='costprocessing',
            name='size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.ProductSize'),
        ),
    ]
