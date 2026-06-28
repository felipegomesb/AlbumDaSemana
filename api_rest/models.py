from django.db import models


class Usuario(models.Model):
    user_username = models.CharField(max_length=100, unique=True, default="")
    user_email = models.EmailField(unique=True, default="", max_length=254)
    user_password = models.CharField(max_length=100, default="")

    def __str__(self):
        return f'Usuario: {self.user_username}, Email: {self.user_email}'


class Musica(models.Model):
    titulo = models.CharField(max_length=200)
    artista = models.CharField(max_length=200)
    album_nome = models.CharField(max_length=200, blank=True, default="")
    genero = models.CharField(max_length=100, blank=True, default="")
    duracao_ms = models.IntegerField(default=0)
    capa_url = models.URLField(blank=True, default="")
    spotify_id = models.CharField(max_length=100, unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titulo} - {self.artista}'

    class Meta:
        verbose_name_plural = "Musicas"


class Album(models.Model):
    titulo = models.CharField(max_length=200)
    artista = models.CharField(max_length=200)
    ano = models.IntegerField(null=True, blank=True)
    genero = models.CharField(max_length=100, blank=True, default="")
    capa_url = models.URLField(blank=True, default="")
    spotify_id = models.CharField(max_length=100, unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titulo} - {self.artista}'

    class Meta:
        verbose_name_plural = "Albuns"


class Faixa(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='faixas')
    titulo = models.CharField(max_length=200)
    duracao_ms = models.IntegerField(default=0)
    numero = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.numero}. {self.titulo}'

    class Meta:
        ordering = ['numero']


class MusicaDoDia(models.Model):
    musica = models.ForeignKey(Musica, on_delete=models.CASCADE)
    data = models.DateField(unique=True)

    def __str__(self):
        return f'{self.data} - {self.musica.titulo}'

    class Meta:
        verbose_name = "Musica do Dia"
        verbose_name_plural = "Musicas do Dia"


class AlbumDaSemana(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    semana_inicio = models.DateField(unique=True)

    def __str__(self):
        return f'Semana {self.semana_inicio} - {self.album.titulo}'

    class Meta:
        verbose_name = "Album da Semana"
        verbose_name_plural = "Albuns da Semana"
