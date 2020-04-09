# Generated by Django 2.2.7 on 2020-04-02 22:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0013_auto_20200402_1446'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='pdcolor',
        ),
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picone', models.ImageField(null=True, upload_to='productimage')),
                ('pictwo', models.ImageField(null=True, upload_to='productimage')),
                ('picthree', models.ImageField(null=True, upload_to='productimage')),
                ('picfour', models.ImageField(null=True, upload_to='productimage')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userproductcolor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]