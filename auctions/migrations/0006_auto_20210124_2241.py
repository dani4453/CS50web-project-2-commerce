# Generated by Django 3.1.5 on 2021-01-25 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='status',
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
