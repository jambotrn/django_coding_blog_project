# Generated by Django 4.0.3 on 2022-08-10 06:49

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('blog', '0013_alter_comment_blog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='tag',
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='Enter the blog keyword', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
