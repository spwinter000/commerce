# Generated by Django 3.1.2 on 2020-11-09 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20201109_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='starting_price',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
