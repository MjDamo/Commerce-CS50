# Generated by Django 4.2.7 on 2023-11-26 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='item_comment', to='auctions.comment'),
        ),
    ]
