# Generated by Django 3.1 on 2023-11-09 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=10)),
                ('room_interest', models.TextField(blank=True, default=None, null=True)),
            ],
        ),
    ]
