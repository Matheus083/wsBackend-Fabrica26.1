import os
from datetime import date

import requests
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from spacelog.models import AstronomyPicture

 
# Tempo máximo de espera pela API da NASA (segundos).
REQUEST_TIMEOUT = 10

class Command(BaseCommand):
    help = 'Fetches Astronomy Picture of the Day from the NASA API'

# Declaração dos argumentos aceitos pelo comando.
    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            default=None,
            metavar='YYYY-MM-DD',
            help=("Date of the APOD to search for (YYYY-MM-DD)"
                  "Omit this to use today's date."
                ),
        )
        parser.add_argument(
            '--force',
            action='store_true',
            default=False,
            help='Overwrite existing APOD if it exists',
        )

# Ponto de entrada principal.(Coração do comando).
    def handle(self, *args, **options):
        target_date = self._resolve_date(options['date'])
        api_key = self._get_api_key()

        self.stdout.write(f'Fetching APOD for {target_date}...')
        
        data = self._fetch_from_nasa(api_key, target_date)
        self._save_to_database(data, force=options['force'])

# Helpers privados - cada um faz exatamente uma coisa.
    def _resolve_date(self, raw_date: str | None) -> str:
        ''' Converte a string de data ou retorna hoje. '''
        if raw_date is None:
            return date.today()
        
        try:
            return date.fromisoformat(raw_date)
        except ValueError:
            # CommandError interrompe o comando e imprime a mensagem de erro.
            # Formatada pelo Django, sem stack trace desnecessário.
            raise CommandError(f'Invalid date format: "{raw_date}". Use YYYY-MM-DD.')
    def _get_api_key(self) -> str:
        """
        Lê a chave da NASA a partir da variável de ambiente.
 
        O python-dotenv já carregou o .env no settings.py, então
        os.environ está populado quando chegamos aqui.
        """
        api_key = os.environ.get('NASA_API_KEY')
        if not api_key:
            raise CommandError(
                'NASA_API_KEY NOT FOUND. '
                'Add the NASA API key to your .env file.'
            )                    
        return api_key
    
    def _fetch_from_nasa(self, api_key: str, targe_date: date) -> dict:
        """
        Chama a API APOD da NASA e retorna o payload como dicionário.
        Trata os erros HTTP de forma descritiva para facilitar o debug.
        """
        url = 'https://api.nasa.gov/planetary/apod'
        params = {
            'api_key': api_key,
            'date': targe_date.isoformat(), 
        } 
    
        try: 
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        except requests.exceptions.ConnectionError:
            raise CommandError('Connection error. Check your internet connection.')
        except requests.exceptions.Timeout:
            raise CommandError(
                f'The NASA API is not responding in {REQUEST_TIMEOUT}s. try again later.'
            )
    
        # Trata erros HTTP com mensagens claras.
        if response.status_code == 400:
            raise CommandError(
                f'Date invalid for api of the Nasa: {targe_date}.'
                f'The APOD exists for the 1995-06-16.'
            )
        if response.status_code == 403:
            raise CommandError(
                'The NASA API key is not valid. '
                'Add the NASA API key to your .env file.'
            )
        if response.status_code == 429:
            raise CommandError(
                'Limit of requests exceeded (rate limit).'
                'DEMO_KEY: 30/hour. Register for a key at https://api.nasa.gov/'
            )
        if not response.ok:
            raise CommandError(
                f"Error unexpected of the API NASA: {response.status_code}."
            )
        
        return response.json()
    
    def _save_to_database(self, data: dict, force: bool) -> None:
        '''
        Salva o APOD no banco evitando duplicatas.
 
        Estratégia: usa get_or_create com o campo 'date' como chave única.
        Se o registro já existe e --force não foi passado, apenas informa.
        Se --force foi passado, atualiza os campos.
        '''
        apod_date_str = data.get('date')
        if not apod_date_str:
            raise CommandError('API response missing "date" field. Unexpected data.')
        
        # Campos que serão criados ou atualizados.
        defaults = {
            'title': data.get('title', ''),
            'explanation': data.get('explanation', ''),
            'url': data.get('url', ''),
            # A NASA retorna "image" ou "video", salva o que vier.
            'media_type': data.get('media_type', ''),
        }

        try:
            picture, created = AstronomyPicture.objects.get_or_create(
                date=apod_date_str,
                defaults=defaults,
            )
        except IntegrityError as exec:
            # Captura race conditions em ambientes com workers concorrentes.
            raise CommandError(f'Conflict when saving at the bank. {exec}')
            
        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'[CREATED] "{picture.date}" - "{picture.title}"'
                )
            )

        elif force:
            # Atualiza os campos manualmente quando --force é usado.
            for field, value in defaults.items():
                setattr(picture, field, value)
            picture.save()
            self.stdout.write(
                self.style.WARNING(
                    f'[UPDATED] "{picture.date}" - "{picture.title}"'
                )
            )
            
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'[IS ALREADY EXISTS] "{picture.date}" - "{picture.title}"). '
                    'Use --force to overwrite.'
                )
            )