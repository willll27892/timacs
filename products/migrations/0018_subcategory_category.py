# Generated by Django 2.2.7 on 2020-05-15 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_tracker_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='products.Category'),
        ),
    ]
