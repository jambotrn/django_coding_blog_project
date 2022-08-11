# Generated by Django 4.0.3 on 2022-07-16 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='avater',
            field=models.ImageField(default='default.jpg', upload_to='profile_pictures'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fullname',
            field=models.CharField(help_text='Write your full name', max_length=200),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pictures'),
        ),
    ]
