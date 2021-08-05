from django.db import models


class Video(models.Model):
    nombre = models.CharField(max_length=100)
    #duracion = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/video/')
    #cover = models.ImageField(upload_to='videos/covers/', null=True, blank=True)

    def __str__(self):
        return self.nombre

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)
