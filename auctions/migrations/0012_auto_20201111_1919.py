# Generated by Django 3.1.2 on 2020-11-12 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20201111_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='watchlist',
            field=models.BooleanField(),
        ),
    ]