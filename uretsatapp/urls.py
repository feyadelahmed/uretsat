from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("anasayfa/", views.index, name="index"),
    path("giris/", views.giris, name="giris"),
    path("kayit/", views.kayit, name="kayit"),
    path("cikis/", views.cikis, name="cikis"),
    path("profil/", views.profil, name="profil"),
    path("profilResimKaldir/", views.profilResimKaldir, name="profilResimKaldir"),
    path("urunEkle/", views.urunEkle, name="urunEkle"),
    path("urunSil/<int:id>/", views.urunSil, name="urunSil"),
    path("urunlerim/", views.urunlerim, name="urunlerim"),
    path("alisveris/", views.alisveris, name="alisveris"),
    path("sepet/", views.sepet, name="sepet"),
    path("sepet/ekle/<int:id>/", views.sepetEkle, name="sepetEkle"),
    path("sepet/sil/<int:id>/", views.sepetSil, name="sepetSil"),
    path("odeme/", views.odeme, name="odeme"),
    path("siparislerim/", views.siparislerim, name="siparislerim"),
    path("rate/<int:id>/", views.rate, name="rate"),
    path("urun/<int:id>/", views.urun, name="urun"),
    path("urunDuzenle/<int:id>/", views.urunDuzenle, name="urunDuzenle"),
]