# Generated by Django 4.2.7 on 2024-09-25 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ads3', '0008_color_size_productvaraint_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product_variant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ads3.productvaraint'),
            preserve_default=False,
        ),
    ]
