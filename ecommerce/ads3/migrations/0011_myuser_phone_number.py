# Generated by Django 4.2.7 on 2024-09-30 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads3', '0010_brand_remove_cartitem_cart_remove_cartitem_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='phone_number',
            field=models.IntegerField(default='0917294596'),
            preserve_default=False,
        ),
    ]
