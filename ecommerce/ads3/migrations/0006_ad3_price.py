# Generated by Django 4.2.7 on 2024-09-21 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads3', '0005_remove_ad3_price_productvaraint'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad3',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
    ]
