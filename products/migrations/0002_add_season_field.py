# Generated migration to add season field to Product
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='season',
            field=models.CharField(choices=[('spring', 'Spring'), ('summer', 'Summer'), ('autumn', 'Autumn'), ('winter', 'Winter'), ('all', 'All-season')], default='all', max_length=10, blank=True),
        ),
    ]
