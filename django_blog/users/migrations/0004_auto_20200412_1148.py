# Generated by Django 3.0.5 on 2020-04-12 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200411_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='progile_pics'),
        ),
    ]
