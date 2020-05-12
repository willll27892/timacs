# Generated by Django 2.2.7 on 2020-05-07 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0023_receiversname_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receiversname',
            name='order',
        ),
        migrations.AddField(
            model_name='productorder',
            name='receivername',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='order.ReceiversName'),
        ),
    ]
