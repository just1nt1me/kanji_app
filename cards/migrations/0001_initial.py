# Generated by Django 4.2.6 on 2023-10-11 06:35

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
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expression', models.CharField(max_length=100)),
                ('reading', models.CharField(max_length=100)),
                ('meaning', models.CharField(max_length=100)),
                ('box', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('tags', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.jlptlevel')),
            ],
        ),
    ]
