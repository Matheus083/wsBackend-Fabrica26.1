from django.db import models

# Definição do modelo do banco de dados.  
class AstronomyPicture(models.Model):
    title = models.CharField(max_length=255)
    explanation = models.TextField()
    date = models.DateField(unique=True) # Impede datas repetidas.
    url = models.URLField()
    media_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.title}"
