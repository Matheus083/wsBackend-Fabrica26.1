from django.views.generic import ListView
from spacelog.models import AstronomyPicture

class APODListView(ListView):
    model = AstronomyPicture
    template_name = 'spacelog/diario.html' # Onde o HTML vai morar
    context_object_name = 'pictures' # O nome da lista dentro do HTML
    ordering = ['-date'] # O "-" significa do mais novo para o mais antigo
    paginate_by = 10 # Se tiver 100 fotos, ele cria páginas de 10