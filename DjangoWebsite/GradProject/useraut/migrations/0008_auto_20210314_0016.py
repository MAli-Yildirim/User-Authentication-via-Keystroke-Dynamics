# Generated by Django 3.1.7 on 2021-03-13 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('useraut', '0007_data_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='data',
            old_name='password',
            new_name='passwor',
        ),
    ]