# Generated by Django 4.0.3 on 2022-08-10 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_remove_blog_tag_blog_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=250, null=True),
        ),
    ]
