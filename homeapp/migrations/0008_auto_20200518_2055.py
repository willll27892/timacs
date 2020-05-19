# Generated by Django 2.2.7 on 2020-05-19 03:55

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0007_auto_20200515_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', ckeditor.fields.RichTextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='deliveryandreturnpolicies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy', ckeditor.fields.RichTextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='privacypolicies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy', ckeditor.fields.RichTextField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='sagreement',
            name='agreement',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]
