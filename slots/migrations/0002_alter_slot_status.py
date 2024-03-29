# Generated by Django 4.2 on 2023-06-16 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slots', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='status',
            field=models.CharField(choices=[('free', 'FREE'), ('booked', 'BOOKED')], default='FREE', help_text='Slot status', max_length=10),
        ),
    ]
