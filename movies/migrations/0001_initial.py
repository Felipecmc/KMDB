# Generated by Django 4.1.2 on 2022-10-17 23:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('genres', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=127)),
                ('duration', models.CharField(max_length=10)),
                ('premiere', models.DateTimeField()),
                ('classification', models.IntegerField()),
                ('synopsis', models.TextField()),
                ('genre', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='genres.genre')),
            ],
        ),
    ]
