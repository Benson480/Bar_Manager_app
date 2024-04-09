# Generated by Django 5.0.4 on 2024-04-09 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_itemimage_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item_price',
            name='Unit_Of_Measure',
            field=models.CharField(choices=[('Kg', 'Kg'), ('Ltr', 'Ltr'), ('Bag', 'Bag'), ('Pcs', 'Pcs'), ('Pcs', 'Pc'), ('Carton', 'Carton'), ('Pkt', 'Pkt'), ('Tons', 'Tons'), ('Bottles', 'Bottles'), ('Dose', 'Dose'), ('Course', 'Course'), ('Square Meter', 'Square Meter'), ('Case', 'Case')], db_index=True, max_length=255, null=True),
        ),
    ]
