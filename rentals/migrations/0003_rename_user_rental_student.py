# Generated by Django 5.0.3 on 2024-03-17 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0002_student_alter_rental_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rental',
            old_name='user',
            new_name='student',
        ),
    ]