# Generated by Django 3.1.2 on 2020-10-04 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
                ('belongsto', models.IntegerField(default=0)),
                ('visibility', models.CharField(max_length=100)),
            ],
        ),
    ]