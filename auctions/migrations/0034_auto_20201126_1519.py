# Generated by Django 3.1.2 on 2020-11-26 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0033_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='listings',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='listings',
            field=models.ManyToManyField(blank=True, to='auctions.AuctionListing'),
        ),
    ]