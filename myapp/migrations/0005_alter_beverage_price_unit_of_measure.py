# Generated by Django 4.1.7 on 2024-03-23 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_beverage_price_unit_of_measure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beverage_price',
            name='Unit_Of_Measure',
            field=models.CharField(choices=[('Kg', 'Kg'), ('Ltr', 'Ltr'), ('Bag', 'Bag'), ('Pcs', 'Pcs'), ('Pcs', 'Pc'), ('Carton', 'Carton'), ('Pkt', 'Pkt'), ('Tons', 'Tons'), ('Bottles', 'Bottles'), ('Dose', 'Dose'), ('Course', 'Course')], db_index=True, max_length=255, null=True),
        ),
    ]
