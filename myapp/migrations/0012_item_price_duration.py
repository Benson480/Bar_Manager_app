# Generated by Django 5.0.4 on 2024-04-22 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_softwarerequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='item_price',
            name='Duration',
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
    ]
