# Generated by Django 3.1.7 on 2021-04-23 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Finance', '0011_auto_20210423_0406'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='eventmember',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='eventmember',
            name='event',
        ),
        migrations.RemoveField(
            model_name='eventmember',
            name='user',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.DeleteModel(
            name='EventMember',
        ),
    ]
