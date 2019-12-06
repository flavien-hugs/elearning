# Generated by Django 3.0 on 2019-12-06 01:00

import cours.champs
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cours', '0002_contenufichier_contenuimage_contenus_contenutext_contenuvideo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contenus',
            options={'ordering': ['ordre'], 'verbose_name': 'Contenu'},
        ),
        migrations.AlterModelOptions(
            name='cours',
            options={'ordering': ['-date_de_creation'], 'verbose_name': 'Cours'},
        ),
        migrations.AlterModelOptions(
            name='matieres',
            options={'ordering': ['title'], 'verbose_name': 'Matière'},
        ),
        migrations.AlterModelOptions(
            name='modules',
            options={'ordering': ['ordre'], 'verbose_name': 'Module'},
        ),
        migrations.AddField(
            model_name='contenus',
            name='ordre',
            field=cours.champs.ChampsPerso(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='modules',
            name='ordre',
            field=cours.champs.ChampsPerso(blank=True, default=2),
            preserve_default=False,
        ),
    ]
