# Generated by Django 3.0 on 2019-12-05 20:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Titre du Cours')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='URL')),
                ('resume', models.TextField()),
                ('date_de_creation', models.DateField(auto_now_add=True, verbose_name='Date de création du Cours')),
                ('instructeur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_de_creation'],
            },
        ),
        migrations.CreateModel(
            name='Matieres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='Matière du Cours')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='URL')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Modules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Titre du Module')),
                ('description', models.TextField(blank=True, verbose_name='Description du Cours')),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cours.Cours')),
            ],
        ),
        migrations.AddField(
            model_name='cours',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cours.Matieres'),
        ),
    ]