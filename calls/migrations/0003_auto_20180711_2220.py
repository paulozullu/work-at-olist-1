# Generated by Django 2.0.7 on 2018-07-12 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0002_auto_20180710_1334'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='phonecall',
            unique_together={('type', 'call_id')},
        ),
    ]