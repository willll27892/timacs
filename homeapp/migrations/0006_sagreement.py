# Generated by Django 2.2.7 on 2020-05-14 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0005_activity_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sagreement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agreement', models.TextField(null=True)),
            ],
        ),
    ]
