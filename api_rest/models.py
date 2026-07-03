from django.db import models


class Usuario(models.Model):
    user_username = models.CharField(max_length=100, unique=True, default="")
    user_email = models.EmailField(unique=True, default="", max_length=254)
    user_password = models.CharField(max_length=100, default="")
    user_bio = models.TextField(blank=True, default="")
    user_avatar = models.FileField(upload_to='avatars/', blank=True, null=True)
    is_admin = models.BooleanField(default=False)

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
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
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
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
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


class Review(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
    )
    autor_nome = models.CharField(max_length=100)
    musica = models.ForeignKey(
        Musica,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reviews_musicas',
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reviews_albuns',
    )
    texto = models.TextField()
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        alvo = self.musica or self.album
        return f'{self.autor_nome} - {alvo}'

    class Meta:
        ordering = ['-criado_em']


class Reacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    musica = models.ForeignKey(Musica, on_delete=models.CASCADE, null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=10)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'musica'], name='unique_reacao_musica', condition=models.Q(musica__isnull=False)),
            models.UniqueConstraint(fields=['usuario', 'album'], name='unique_reacao_album', condition=models.Q(album__isnull=False)),
            models.UniqueConstraint(fields=['usuario', 'review'], name='unique_reacao_review', condition=models.Q(review__isnull=False)),
        ]
