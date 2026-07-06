from datetime import date, timedelta

from django.core.management.base import BaseCommand

from api_rest.models import Musica, MusicaDoDia


class Command(BaseCommand):
    help = 'Seleciona a musica do dia automaticamente, evitando repeticoes nos ultimos 30 dias'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data',
            type=str,
            default=None,
            help='Data alvo no formato YYYY-MM-DD (padrao: hoje)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Substitui a musica mesmo se ja existir uma para a data',
        )

    def handle(self, *args, **options):
        if options['data']:
            alvo = date.fromisoformat(options['data'])
        else:
            alvo = date.today()

        existente = MusicaDoDia.objects.filter(data=alvo).first()
        if existente and not options['force']:
            self.stdout.write(
                f'Musica do dia {alvo}: "{existente.musica.titulo}" (ja definida)'
            )
            return

        trinta_dias_atras = alvo - timedelta(days=30)
        ids_recentes = MusicaDoDia.objects.filter(
            data__gte=trinta_dias_atras
        ).values_list('musica_id', flat=True)

        disponiveis = Musica.objects.exclude(id__in=ids_recentes)
        if not disponiveis.exists():
            disponiveis = Musica.objects.all()

        if not disponiveis.exists():
            self.stderr.write('Nenhuma musica cadastrada no banco')
            return

        musica_escolhida = disponiveis.order_by('?').first()

        if existente:
            existente.musica = musica_escolhida
            existente.save()
        else:
            MusicaDoDia.objects.create(musica=musica_escolhida, data=alvo)

        self.stdout.write(
            f'Musica do dia {alvo}: "{musica_escolhida.titulo}" - {musica_escolhida.artista}'
        )
