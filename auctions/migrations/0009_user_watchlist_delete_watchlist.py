# Generated by Django 4.2.7 on 2023-11-25 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_bid_user_alter_bid_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watchlist_users', to='auctions.listing'),
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]
