# Generated by Django 5.0.3 on 2024-07-02 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uretsatapp', '0005_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rate',
            name='siparis',
        ),
    ]