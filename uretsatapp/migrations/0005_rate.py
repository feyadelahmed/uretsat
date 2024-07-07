# Generated by Django 5.0.3 on 2024-07-02 13:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uretsatapp', '0004_siparisler'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField()),
                ('siparis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uretsatapp.siparisler')),
                ('urun', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uretsatapp.urun')),
            ],
        ),
    ]
