# Generated by Django 4.2.7 on 2024-09-30 22:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ads3', '0012_alter_myuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverorder',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driverorder', to='ads3.order'),
        ),
    ]
