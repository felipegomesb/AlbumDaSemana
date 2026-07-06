from datetime import date, timedelta

from django.core.management.base import BaseCommand

from api_rest.models import Album, AlbumDaSemana


class Command(BaseCommand):
    help = 'Seleciona o album da semana automaticamente, evitando repeticoes nos ultimos 60 dias'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data',
            type=str,
            default=None,
            help='Data de referencia no formato YYYY-MM-DD (padrao: hoje)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Substitui o album mesmo se ja existir um para a semana',
        )

    def handle(self, *args, **options):
        if options['data']:
            ref = date.fromisoformat(options['data'])
        else:
            ref = date.today()

        segunda = ref - timedelta(days=ref.weekday())

        existente = AlbumDaSemana.objects.filter(semana_inicio=segunda).first()
        if existente and not options['force']:
            self.stdout.write(
                f'Album da semana {segunda}: "{existente.album.titulo}" (ja definido)'
            )
            return

        sessenta_dias_atras = ref - timedelta(days=60)
        ids_recentes = AlbumDaSemana.objects.filter(
            semana_inicio__gte=sessenta_dias_atras
        ).values_list('album_id', flat=True)

        disponiveis = Album.objects.exclude(id__in=ids_recentes)
        if not disponiveis.exists():
            disponiveis = Album.objects.all()

        if not disponiveis.exists():
            self.stderr.write('Nenhum album cadastrado no banco')
            return

        album_escolhido = disponiveis.order_by('?').first()

        if existente:
            existente.album = album_escolhido
            existente.save()
        else:
            AlbumDaSemana.objects.create(album=album_escolhido, semana_inicio=segunda)

        self.stdout.write(
            f'Album da semana {segunda}: "{album_escolhido.titulo}" - {album_escolhido.artista}'
        )
