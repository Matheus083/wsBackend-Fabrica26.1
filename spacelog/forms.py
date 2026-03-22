from django import forms
from .models import AstronomyPicture

# Criar um formulário para o modelo AstronomyPicture.
class AstronomyPictureForm(forms.ModelForm):
    # Configurando.
    class Meta:
        model = AstronomyPicture
        fields = ['title', 'date', 'explanation', 'url', 'media_type']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'media_type': forms.Select(choices=[('image', 'Imagem'), ('video', 'Vídeo')], attrs={'class': 'form-control'}),
        }
