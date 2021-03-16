# Generated by Django 3.1.7 on 2021-03-15 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20210315_1006'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articlecategory',
            old_name='category',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=20, unique=True, verbose_name='タグの名前'),
        ),
    ]
