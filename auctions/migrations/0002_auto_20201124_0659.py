# Generated by Django 3.1.3 on 2020-11-24 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='auction',
            field=models.ManyToManyField(blank=True, to='auctions.AuctionList'),
        ),
    ]
