# Generated by Django 3.2.4 on 2021-06-28 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='auth_provider',
            field=models.CharField(blank=True, default='email', max_length=255),
        ),
    ]
