# Generated by Django 5.0.3 on 2024-03-17 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0003_rename_user_rental_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='rental',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
