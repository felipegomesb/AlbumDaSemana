# Generated manually to create the catalog and weekly rotation tables.

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Musica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('artista', models.CharField(max_length=200)),
                ('album_nome', models.CharField(blank=True, default='', max_length=200)),
                ('genero', models.CharField(blank=True, default='', max_length=100)),
                ('duracao_ms', models.IntegerField(default=0)),
                ('capa_url', models.URLField(blank=True, default='')),
                ('spotify_id', models.CharField(max_length=100, unique=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Musicas',
            },
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('artista', models.CharField(max_length=200)),
                ('ano', models.IntegerField(blank=True, null=True)),
                ('genero', models.CharField(blank=True, default='', max_length=100)),
                ('capa_url', models.URLField(blank=True, default='')),
                ('spotify_id', models.CharField(max_length=100, unique=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Albuns',
            },
        ),
        migrations.CreateModel(
            name='Faixa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('duracao_ms', models.IntegerField(default=0)),
                ('numero', models.IntegerField(default=1)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faixas', to='api_rest.album')),
            ],
            options={
                'ordering': ['numero'],
            },
        ),
        migrations.CreateModel(
            name='MusicaDoDia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(unique=True)),
                ('musica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_rest.musica')),
            ],
            options={
                'verbose_name': 'Musica do Dia',
                'verbose_name_plural': 'Musicas do Dia',
            },
        ),
        migrations.CreateModel(
            name='AlbumDaSemana',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semana_inicio', models.DateField(unique=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_rest.album')),
            ],
            options={
                'verbose_name': 'Album da Semana',
                'verbose_name_plural': 'Albuns da Semana',
            },
        ),
    ]