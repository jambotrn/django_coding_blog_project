# Generated by Django 4.0.3 on 2022-08-05 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_comment_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['comment_date']},
        ),
        migrations.RemoveField(
            model_name='blog',
            name='image',
        ),
        migrations.AlterField(
            model_name='comment',
            name='title',
            field=models.CharField(help_text='Enter the subject of your comment', max_length=220, null=True),
        ),
    ]