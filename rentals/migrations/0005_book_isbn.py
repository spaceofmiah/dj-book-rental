# Generated by Django 5.0.3 on 2024-03-17 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0004_rental_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='isbn',
            field=models.CharField(default=1, max_length=225),
            preserve_default=False,
        ),
    ]
