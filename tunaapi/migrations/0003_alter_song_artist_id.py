# Generated by Django 4.1.3 on 2023-12-09 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tunaapi', '0002_rename_label_genre_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='artist_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='tunaapi.artist'),
        ),
    ]
