# Generated by Django 2.2.7 on 2020-05-19 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0010_buyer_terms_and_condition'),
    ]

    operations = [
        migrations.CreateModel(
            name='contactus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('phone', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
