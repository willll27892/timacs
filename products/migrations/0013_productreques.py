# Generated by Django 2.2.7 on 2020-05-10 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0004_sellerid_verified'),
        ('products', '0012_auto_20200508_0853'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReques',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('productname', models.CharField(max_length=200, null=True)),
                ('productmodel', models.CharField(max_length=200, null=True)),
                ('description', models.TextField(null=True)),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productrequest', to='homeapp.Sessionlog')),
            ],
        ),
    ]
