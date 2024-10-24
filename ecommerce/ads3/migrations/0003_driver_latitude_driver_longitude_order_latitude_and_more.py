# Generated by Django 4.2.7 on 2024-09-05 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads3', '0002_driverorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='driver',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
