# Generated by Django 3.1.2 on 2020-11-13 01:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20201112_2003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='user',
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='auctions.user'),
            preserve_default=False,
        ),
    ]
