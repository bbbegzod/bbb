from django.db import models

# Create your models here.


class Ishchi(models.Model):
    ism = models.CharField(max_length=120)
    familya = models.CharField(max_length=120)
    jins = models.BooleanField(default=True)
    birth_date = models.DateField()
    lavozim = models.CharField(max_length=120)
    oylik = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.ism} {self.familya}"
