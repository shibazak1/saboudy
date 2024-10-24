# Generated by Django 4.2.7 on 2024-09-02 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ads3', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picked_at', models.DateTimeField(auto_now_add=True)),
                ('delivered_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Picked', 'Picked'), ('In Transit', 'In Transit'), ('Delivered', 'Delivered')], default='Picked', max_length=20)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ads3.driver')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ads3.order')),
            ],
        ),
    ]
