# Generated by Django 3.1.7 on 2021-03-11 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraut', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trainset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('data', models.CharField(max_length=2000000, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='person',
        ),
    ]