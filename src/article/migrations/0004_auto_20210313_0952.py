# Generated by Django 3.1.7 on 2021-03-13 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_article_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='public',
            field=models.BooleanField(default=0, verbose_name='公開状態'),
        ),
    ]
