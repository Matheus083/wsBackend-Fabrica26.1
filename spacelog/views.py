# spacelog/views.py

import logging
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from spacelog.models import AstronomyPicture
from .forms import AstronomyPictureForm
from .fetch_apod import get_nasa_data

# Configura o logger para vermos erros no terminal
logger = logging.getLogger(__name__)

class APODListView(ListView):
    model = AstronomyPicture
    template_name = 'spacelog/diario.html'
    context_object_name = 'pictures'
    ordering = ['-date']
    paginate_by = 10

class APODDetailView(DetailView):
    model = AstronomyPicture
    template_name = 'spacelog/detail.html'
    context_object_name = 'picture'

class APODCreateView(CreateView):
    model = AstronomyPicture
    form_class = AstronomyPictureForm
    template_name = "spacelog/form.html"
    success_url = reverse_lazy("spacelog:apod_list")

    def get_initial(self):
        initial = super().get_initial()
        data_nasa = self.request.GET.get("data_nasa")

        # LOG DE DIAGNÓSTICO 1
        print(f"\n[DEBUG] Tentando buscar data: {data_nasa}")

        if data_nasa:
            try:
                nasa_data = get_nasa_data(data_nasa)
                
                # LOG DE DIAGNÓSTICO 2
                print(f"[DEBUG] Resposta da função get_nasa_data: {nasa_data}")

                if nasa_data:
                    # Mapeamento seguro: tenta hdurl, se não tiver vai url comum
                    url_final = nasa_data.get("hdurl") or nasa_data.get("url")
                    
                    initial.update({
                        "date":        nasa_data.get("date"),
                        "title":       nasa_data.get("title"),
                        "explanation": nasa_data.get("explanation"),
                        "url":         url_final,
                        "media_type":  nasa_data.get("media_type", "image"),
                    })
                    messages.success(self.request, f"Dados da NASA para {data_nasa} carregados!")
                else:
                    messages.warning(self.request, f"A NASA não retornou dados para a data {data_nasa}. Verifique se é uma data futura.")

            except Exception as e:
                # AGORA NÓS VEMOS O ERRO!
                print(f"[ERRO CRÍTICO] Falha ao processar API: {e}")
                logger.error(f"Erro no preenchimento automático: {e}", exc_info=True)
                messages.error(self.request, "Erro técnico ao conectar com a NASA. Tente preencher manualmente.")

        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["prefilled"] = bool(self.request.GET.get("data_nasa"))
        ctx["form_title"] = "Nova Descoberta"
        ctx["submit_label"] = "Salvar no Diário"
        return ctx

class APODUpdateView(UpdateView):
    model = AstronomyPicture
    form_class = AstronomyPictureForm
    template_name = "spacelog/form.html"
    success_url = reverse_lazy('spacelog:apod_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form_title"] = "Editar Registro"
        ctx["submit_label"] = "Atualizar"
        return ctx

class APODDeleteView(DeleteView):
    model = AstronomyPicture
    template_name = "spacelog/confirm_delete.html"
    success_url = reverse_lazy('spacelog:apod_list')
    