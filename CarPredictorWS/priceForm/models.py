from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Marka(models.Model):
    isim = models.CharField(max_length=100)

    def __str__(self):
        return self.isim
class Seri(models.Model):
    seri_adi= models.CharField(max_length=100)

    def __str__(self):
        return self.seri_adi
class Model(models.Model):
    model_adi = models.CharField(max_length=50)

    def __str__(self):
        return self.model_adi
class VitesTipi(models.Model):
    vites_tipi = models.CharField(max_length=50)

    def __str__(self):
        return self.vites_tipi
class YakıtTipi (models.Model):
    yakit_tipi = models.CharField(max_length=50)

    def __str__(self):
        return self.yakit_tipi
class KasaTipi (models.Model):
    kasa_tipi = models.CharField(max_length=50)

    def __str__(self):
        return self.kasa_tipi
class Çekiş (models.Model):
    çekiş_tipi = models.CharField(max_length=50)

    def __str__(self):
        return self.çekiş_tipi
   
class Arac(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    Marka = models.CharField(max_length=100)
    Seri = models.CharField(max_length=100)
    Model = models.CharField(max_length=100)
    Yıl = models.IntegerField()
    Kilometre = models.FloatField()
    VitesTipi = models.CharField(max_length=50)
    YakıtTipi = models.CharField(max_length=50)
    KasaTipi = models.CharField(max_length=50)
    MotorHacmi = models.FloatField()
    MotorGücü = models.FloatField()
    Çekiş = models.CharField(max_length=50)
    OrtYakıtTüketimi = models.FloatField()
    YakıtDeposu = models.FloatField()