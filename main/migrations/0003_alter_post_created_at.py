# Generated by Django 5.0 on 2023-12-25 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
