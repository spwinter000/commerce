# Generated by Django 3.1.2 on 2020-11-29 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0035_auto_20201126_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='image',
            field=models.ImageField(blank=True, default='images/no-image.jpg', upload_to='images/'),
        ),
    ]
