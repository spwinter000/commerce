# Generated by Django 3.1.2 on 2020-11-09 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20201109_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]