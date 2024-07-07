from django.db import models
from django.contrib.auth.models import User


class Kullanici(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tel = models.CharField(max_length=11)
    tur = models.CharField(max_length=10)
    resim = models.TextField()
    konum = models.TextField()

class Urun(models.Model):
    ad = models.CharField(max_length=500)
    tur = models.CharField(max_length=500)
    stok = models.CharField(max_length=500)
    fiyat = models.DecimalField(max_digits=10, decimal_places=2)
    detay = models.TextField()
    resim = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Siparisler(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tamamlandi = models.BooleanField()
    urunler = models.ManyToManyField(Urun)

class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    urun = models.ForeignKey(Urun, on_delete=models.CASCADE)
    rate = models.IntegerField()
