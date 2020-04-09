# Generated by Django 2.2.7 on 2020-04-08 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_tracker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracker',
            name='id',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tracker',
            name='productdisplay',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='display', to='products.Product'),
        ),
    ]