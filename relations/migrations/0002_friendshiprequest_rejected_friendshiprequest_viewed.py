# Generated by Django 4.2.3 on 2023-08-22 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendshiprequest',
            name='rejected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='friendshiprequest',
            name='viewed',
            field=models.BooleanField(default=False),
        ),
    ]
