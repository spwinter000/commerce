# Generated by Django 3.1.2 on 2020-11-24 20:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_auto_20201124_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='time_of_listing',
            field=models.DateTimeField(null=True, auto_now_add=True, blank=True,),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='time_of_listing',
            field=models.DateTimeField(null=True, auto_now_add=True, blank=True,),
            preserve_default=False,
        ),
    ]
