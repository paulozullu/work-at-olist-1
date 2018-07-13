# Generated by Django 2.0.7 on 2018-07-13 01:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('telephone_numbers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('call_id', models.IntegerField(null=True, unique=True)),
                ('call_start_date', models.DateField()),
                ('call_start_time', models.TimeField()),
                ('call_duration', models.DurationField(default=datetime.timedelta(0))),
                ('call_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='telephone_numbers.TelephoneNumber')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='telephone_numbers.TelephoneNumber')),
            ],
        ),
    ]
