# Generated by Django 2.0.7 on 2018-07-10 15:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneCall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('start', 'start'), ('end', 'end')], max_length=5)),
                ('timestamp', models.DateTimeField()),
                ('call_id', models.IntegerField()),
                ('source', models.CharField(default=None, max_length=11, null=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: "9999999999". The first two digits are the area code. The phone number is composed of 8 or 9 digits.', regex='^\\+?1?\\d{10,11}$')])),
                ('destination', models.CharField(default=None, max_length=11, null=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: "9999999999". The first two digits are the area code. The phone number is composed of 8 or 9 digits.', regex='^\\+?1?\\d{10,11}$')])),
            ],
        ),
    ]
