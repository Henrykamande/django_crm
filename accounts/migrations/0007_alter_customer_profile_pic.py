# Generated by Django 3.2.7 on 2021-09-18 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_customer_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default_profile.jpeg', null=True, upload_to=''),
        ),
    ]
