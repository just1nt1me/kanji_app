# Generated by Django 4.2.6 on 2023-10-06 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JLPTLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Kanji',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expression', models.TextField()),
                ('reading', models.TextField()),
                ('meaning', models.TextField()),
                ('tags', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kanji_test.jlptlevel')),
            ],
        ),
    ]
