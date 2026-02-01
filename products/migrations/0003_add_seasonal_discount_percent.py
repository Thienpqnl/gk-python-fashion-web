# Migration to add seasonal_discount_percent to Product
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_add_season_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='seasonal_discount_percent',
            field=models.PositiveIntegerField(default=0, help_text='Seasonal discount percent (0 = no discount)'),
        ),
    ]
