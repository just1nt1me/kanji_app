# Generated by Django 4.2.6 on 2023-12-07 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('level_test', '0002_rename_tags_kanji_jlpt_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kanji',
            name='jlpt_level',
            field=models.CharField(max_length=10),
        ),
        migrations.DeleteModel(
            name='JLPTLevel',
        ),
    ]