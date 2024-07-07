from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Kullanici, Urun, Siparisler, Rate
from django.contrib import messages
import base64

VARSAYILAN_RESIM = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAqkAAAIQCAYAAACi4/d6AAAABHNCSVQICAgIfAhkiAAAIABJREFUeF7t3YlyFMnVgNESDGIb9p2x/f6P40fwAsOAEJvYN/1O+ddYgFB1d2VW3cw8HUGMI9SdlXVuKvxFIzVbf//73/cHDwIECBAgQIAAAQJBBP7Tp8OWSA0yDdsgQIAAAQIECBA4EBCpDgIBAgQIECBAgEA4AZEabiQ2RIAAAQIECBAgIFKdAQIECBAgQIAAgXACIjXcSGyIAAECBAgQIEBApDoDBAgQIECAAAEC4QREariR2BABAgQIECBAgIBIdQYIECBAgAABAgTCCYjUcCOxIQIECBAgQIAAAZHqDBAgQIAAAQIECIQTEKnhRmJDBAgQIECAAAECItUZIECAAAECBAgQCCcgUsONxIYIECBAgAABAgREqjNAgAABAgQIECAQTkCkhhuJDREgQIAAAQIECIhUZ4AAAQIECBAgQCCcgEgNNxIbIkCAAAECBAgQEKnOAAECBAgQIECAQDgBkRpuJDZEgAABAgQIECAgUp0BAgQIECBAgACBcAIiNdxIbIgAAQIECBAgQECkOgMECBAgQIAAAQLhBERquJHYEAECBAgQIECAgEh1BggQIECAAAECBMIJiNRwI7EhAgQIECBAgAABkeoMECBAgAABAgQIhBMQqeFGYkMECBAgQIAAAQIi1RkgQIAAAQIECBAIJyBSw43EhggQIECAAAECBESqM0CAAAECBAgQIBBOQKSGG4kNESBAgAABAgQIiFRngAABAgQIECBAIJyASA03EhsiQIAAAQIECBAQqc4AAQIECBAgQIBAOAGRGm4kNkSAAAECBAgQICBSnQECBAgQIECAAIFwAiI13EhsiAABAgQIECBAQKQ6AwQIECBAgAABAuEERGq4kdgQAQIECBAgQICASHUGCBAgQIAAAQIEwgmI1HAjsSECBAgQIECAAAGR6gwQIECAAAECBAiEExCp4UZiQwQIECBAgAABAiLVGSBAgAABAgQIEAgnIFLDjcSGCBAgQIAAAQIERKozQIAAAQIECBAgEE5ApIYbiQ0RIECAAAECBAiIVGeAAAECBAgQIEAgnIBIDTcSGyJAgAABAgQIEBCpzgABAgQIECBAgEA4AZEabiQ2RIAAAQIECBAgIFKdAQIECBAgQIAAgXACIjXcSGyIAAECBAgQIEBApDoDBAgQIECAAAEC4QREariR2BABAgQIECBAgIBIdQYIECBAgAABAgTCCYjUcCOxIQIECBAgQIAAAZHqDBAgQIAAAQIECIQTEKnhRmJDBAgQIECAAAECItUZIECAAAECBAgQCCcgUsONxIYIECBAgAABAgREqjNAgAABAgQIECAQTkCkhhuJDREgQIAAAQIECIhUZ4AAAQIECBAgQCCcgEgNNxIbIkCAAAECBAgQEKnOAAECBAgQIECAQDgBkRpuJDZEgAABAgQIECAgUp0BAgQIECBAgACBcAIiNdxIbIgAAQIECBAgQECkOgMECBAgQIAAAQLhBERquJHYEAECBAgQIECAgEh1BggQIECAAAECBMIJiNRwI7EhAgQIECBAgAABkeoMECBAgAABAgQIhBMQqeFGYkMECBAgQIAAAQIi1RkgQIAAAQIECBAIJyBSw43EhggQIECAAAECBESqM0CAAAECBAgQIBBOQKSGG4kNESBAgAABAgQIiFRngAABAgQIECBAIJyASA03EhsiQIAAAQIECBAQqc4AAQIECBAgQIBAOAGRGm4kNkSAAAECBAgQICBSnQECBAgQIECAAIFwAiI13EhsiAABAgQIECBAQKQ6AwQIECBAgAABAuEERGq4kdgQAQIECBAgQICASHUGCBAgQIAAAQIEwgmI1HAjsSECBAgQIECAAAGR6gwQIECAAAECBAiEExCp4UZiQwQIECBAgAABAiLVGSBAgAABAgQIEAgnIFLDjcSGCBAgQIAAAQIERKozQIAAAQIECBAgEE5ApIYbiQ0RIECAAAECBAiIVGeAAAECBAgQIEAgnIBIDTcSGyJAgAABAgQIEBCpzgABAgQIECBAgEA4AZEabiQ2RIAAAQIECBAgIFKdAQIECBAgQIAAgXACIjXcSGyIAAECBAgQIEBApDoDBAgQIECAAAEC4QREariR2BABAgQIECBAgIBIdQYIECBAgAABAgTCCYjUcCOxIQIECBAgQIAAAZHqDBAgQIAAAQIECIQTEKnhRmJDBAgQIECAAAECItUZIECAAAECBAgQCCcgUsONxIYIECBAgAABAgREqjNAgAABAgQIECAQTkCkhhuJDREgQIAAAQIECIhUZ4AAAQIECBAgQCCcgEgNNxIb+l7g1KlTw/7+/sEfDwIECBAgQKAP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RGouSesQIECAAAECBAhkExCp2SgtRIAAAQIECBAgkEtApOaStA4BAgQIECBAgEA2AZGajdJCBAgQIECAAAECuQREai5J6xAgQIAAAQIECGQTEKnZKC1EgAABAgQIECCQS0Ck5pK0DgECBAgQIECAQDYBkZqN0kIECBAgQIAAAQK5BERqLknrECBAgAABAgQIZBMQqdkoLUSAAAECBAgQIJBLQKTmkrQOAQIECBAgQIBANgGRmo3SQgQIECBAgAABArkERGouSesQIECAAAECBAhkExCp2SgtRIAAAQIECBAgkEtApOaStA4BAgQIECBAgEA2AZGajdJCBAgQIECAAAECuQREai5J6xAgQIAAAQIECGQTEKnZKC1EgAABAgQIECCQS0Ck5pK0DgECBAgQIECAQDYBkZqN0kIECBAgQIAAAQK5BERqLknrECBAgAABAgQIZBMQqdkoLUSAAAECBAgQIJBLQKTmkrQOAQIECBAgQIBANgGRmo3SQgQIECBAgAABArkERGouSesQIECAAAECBAhkExCp2SgtRIAAAQIECBAgkEtApOaStA4BAgQIECBAgEA2AZGajdJCBAgQIECAAAECuQREai5J6xAgQIAAAQIECGQTEKnZKC1EgAABAgQIECCQS0Ck5pK0DgECBAgQIECAQDYBkZqN0kIECBAgQIAAAQK5BERqLknrECBAgAABAgQIZBMQqdkoLUSAAAECBAgQIJBLQKTmkrQOAQIECBAgQIBANgGRmo3SQgQIECBAgAABArkERGouSesQIECAAAECBAhkExCp2SgtRIAAAQIECBAgkEtApOaStA4BAgQIECBAgEA2AZGajdJCBAgQIECAAAECuQRSpP4fskZPaQOKcT4AAAAASUVORK5CYII="

def index(request):
    return render(request, "uretsatapp/index.html")

def giris(request):
    if request.user.is_authenticated:
        return redirect("/profil")
    
    if request.method != "POST":
        return render(request, "uretsatapp/giris.html")

    context = {}
    kullaniciadi = request.POST["kullaniciadi"].strip()
    sifre = request.POST["sifre"].strip()
    context["bilgiler"] = {
        "kullaniciadi": kullaniciadi,
        "sifre": sifre,
    }

    hata = False
    if not kullaniciadi:
        messages.error(request, "kullanıcıadı boş olamaz")
        hata = True
    elif not sifre:
        messages.error(request, "şifre boş olamaz")
        hata = True

    if hata:
        return render(request, "uretsatapp/giris.html", context)
    
    user = authenticate(username=kullaniciadi, password=sifre)
    if user is None:
        messages.error(request, "kullaniciadi veya şifre yanlıştir.")
        return render(request, "uretsatapp/giris.html", context)

    login(request, user)
    if request.user.kullanici.tur == "esnaf":
        return redirect("/alisveris")
    else:
        return redirect("/urunlerim")


def kayit(request):
    if request.user.is_authenticated:
        return redirect("/profil")

    if request.method != "POST":
        return render(request, "uretsatapp/kayit.html")

    context = {}
    ad = request.POST["ad"].strip()
    soyad = request.POST["soyad"].strip()
    kullaniciadi = request.POST["kullaniciadi"].strip()
    sifre = request.POST["sifre"].strip()
    tel = request.POST["tel"].strip()
    tur = request.POST["tur"].strip()

    context["bilgiler"] = {
        "ad": ad,
        "soyad": soyad,
        "kullaniciadi": kullaniciadi,
        "sifre": sifre,
        "tel": tel,
        "tur": tur,
    }

    hata = False
    if not ad:
        hata = True
        messages.error(request, "ad boş olamaz")
    elif not soyad:
        hata = True
        messages.error(request, "soyad boş olamaz")
    elif not kullaniciadi:
        hata = True
        messages.error(request, "kullanıcıadı boş olamaz")
    elif not sifre:
        hata = True
        messages.error(request, "şifre boş olamaz")
    elif not tel:
        hata = True
        messages.error(request, "tel boş olamaz")
    if hata:
        return render(request, "uretsatapp/kayit.html", context)
    
    kullanici = User.objects.filter(username=kullaniciadi)
    if len(kullanici) != 0:
        messages.error(request, "kullaniciadi zaten mevcüt.")
        return render(request, "uretsatapp/kayit.html", context)

    user = User.objects.create_user(username=kullaniciadi, password=sifre)
    Kullanici.objects.create(user=user)
    user.first_name = ad
    user.last_name = soyad
    user.kullanici.tur = tur
    user.kullanici.tel = tel
    user.kullanici.resim = VARSAYILAN_RESIM
    user.kullanici.save()
    user.save()
    messages.success(request, "Hesap Oluşturuldu.")
    return redirect("/giris")

def cikis(request):
    logout(request)
    return redirect("/giris")

def profil(request):
    if not request.user.is_authenticated:
        return redirect("/giris")

    if request.method != "POST":
        context = {
            "kullaniciadi": request.user.username,
            "ad": request.user.first_name,
            "soyad": request.user.last_name,
            "konum": request.user.kullanici.konum,
            "tel": request.user.kullanici.tel,
            "resim": request.user.kullanici.resim,
        }
        if request.user.kullanici.tur == "esnaf":
            return render(request, "uretsatapp/esnafProfil.html", context)
        else:
            return render(request, "uretsatapp/ureticiProfil.html", context)

    ad = request.POST["ad"].strip()
    soyad = request.POST["soyad"].strip()
    konum = request.POST["konum"].strip()
    tel = request.POST["tel"].strip()
    resim = request.FILES.get("resim")

    user = request.user
    if ad: user.first_name = ad
    if soyad: user.last_name = soyad
    if konum: user.kullanici.konum = konum
    if tel: user.kullanici.tel = tel
    if resim:
        base64_resim = f"data:image/*;base64,{base64.b64encode(resim.read()).decode("utf-8")}"
        user.kullanici.resim = base64_resim

    user.kullanici.save()
    user.save() 

    eskisifre = request.POST["eskisifre"].strip()
    yenisifre = request.POST["yenisifre"].strip()
    if eskisifre and yenisifre:
        u = authenticate(username=request.user.username, password=eskisifre)
        if u is not None:
            request.user.set_password(yenisifre)
            request.user.save()
            messages.success(request, "şifre değiştirildi")
        else:
            messages.error(request, "eski şifre yanlıştır")

    messages.success(request, "profil bilgileri güncellendi")
    return redirect("/profil")

def profilResimKaldir(request):
    if request.user.is_authenticated:
        request.user.kullanici.resim = VARSAYILAN_RESIM
        request.user.kullanici.save()
        messages.success(request, "profil resmi kaldırıldı")
    return redirect("/profil")

def urunlerim(request):
    if not request.user.is_authenticated or request.user.kullanici.tur != "uretici":
        return redirect("/giris")
    context = {}
    urunler = list(request.user.urun_set.all())
    context["urunler"] = urunler
    return render(request, "uretsatapp/urunlerim.html", context)

def urunEkle(request):
    if not request.user.is_authenticated or request.user.kullanici.tur != "uretici":
        return redirect("/giris")
    
    if request.method != "POST":
        return render(request, "uretsatapp/urunEkle.html")
    
    ad = request.POST["ad"].strip()
    tur = request.POST["tur"].strip()
    stok = request.POST["stok"].strip()
    fiyat = request.POST["fiyat"].strip()
    detay = request.POST["detay"].strip()
    resim = request.FILES.get("resim")

    try:
        float(fiyat)
    except ValueError:
        messages.success(request, "fiyat rakamlardan oluşmalı.")
        return render(request, "uretsatapp/urunEkle.html")

    resim_64 = VARSAYILAN_RESIM
    if resim:
        base64_resim = f"data:image/*;base64,{base64.b64encode(resim.read()).decode("utf-8")}"
        resim_64 = base64_resim

    urun = Urun.objects.create(ad=ad, tur=tur, stok=stok, fiyat=fiyat, detay=detay, resim=resim_64, user=request.user)

    return redirect("/urunlerim")

def urunSil(request, id):
    if not request.user.is_authenticated or request.user.kullanici.tur != "uretici":
        return redirect("/giris")
    
    urun = Urun.objects.filter(id=id)
    if len(urun) > 0 and urun[0].user.id == request.user.id:
        urun[0].delete()
    return redirect("/urunlerim")

def urunDuzenle(request, id):
    if not request.user.is_authenticated or request.user.kullanici.tur != "uretici":
        return redirect("/giris")
    
    urunler = Urun.objects.filter(id=id)
    if len(urunler) <= 0 or urunler[0].user.id != request.user.id:
        return redirect("/urunlerim")

    urun = urunler[0]
    context = {}
    context["id"] = urun.id
    context["ad"] = urun.ad
    context["tur"] = urun.tur
    context["stok"] = urun.stok
    context["fiyat"] = urun.fiyat
    context["detay"] = urun.detay
    context["resim"] = urun.resim
    if request.method == "GET":
            return render(request, "uretsatapp/urunDuzenle.html", context)

    elif request.method == "POST":
        ad = request.POST["ad"].strip()
        tur = request.POST["tur"].strip()
        stok = request.POST["stok"].strip()
        fiyat = request.POST["fiyat"].strip()
        detay = request.POST["detay"].strip()
        resim = request.FILES.get("resim")

        try:
            float(fiyat)
        except ValueError:
            messages.success(request, "fiyat rakamlardan oluşmalı.")
            return render(request, "uretsatapp/urunDuzenle.html", context)

        if ad: urun.ad = ad
        if tur: urun.tur = tur
        if stok: urun.stok = stok
        if detay: urun.detay = detay
        if fiyat: urun.fiyat = fiyat

        if resim:
            base64_resim = f"data:image/*;base64,{base64.b64encode(resim.read()).decode("utf-8")}"
            urun.resim = base64_resim

        urun.save()
        return redirect("/urunlerim")

def alisveris(request):
    if not request.user.is_authenticated or request.user.kullanici.tur != "esnaf":
        return redirect("/giris")
    
    urunler_db = list(Urun.objects.all())
    context = {}

    urunler = []

    for u in urunler_db:
        urun = {
            "id": u.id,
            "ad": u.ad,
            "tur": u.tur,
            "stok": u.stok,
            "fiyat": u.fiyat,
            "detay": u.detay,
            "resim": u.resim,
        }

        rate = 0
        rate_db = Rate.objects.filter(urun=u)
        rate_total = 0
        for r in rate_db:
            rate_total = rate_total + r.rate

        if (len(rate_db) > 0):
            rate = rate_total / len(rate_db)
        urun["rate"] = int(rate)
        urunler.append(urun)

    context["urunler"] = urunler
    return render(request, "uretsatapp/alisveris.html", context)

def urun(request, id):
    urunler = Urun.objects.filter(id=id)
    if len(urunler) <= 0:
        return redirect("/alisveris")

    urun = urunler[0]
    context = {}
    context["id"] = urun.id
    context["ad"] = urun.ad
    context["tur"] = urun.tur
    context["stok"] = urun.stok
    context["fiyat"] = urun.fiyat
    context["detay"] = urun.detay
    context["resim"] = urun.resim
    context["uretici"] = urun.user.username
    return render(request, "uretsatapp/urun.html", context)

def sepet(request):
    if not request.user.is_authenticated:
        return redirect("/giris")
    
    sepet = Siparisler.objects.filter(user=request.user, tamamlandi=False)
    if len(sepet) == 0:
        return render(request, "uretsatapp/sepet.html")
    else:
        urunler = list(sepet[0].urunler.all())
        context = {}
        context["urunler"] = urunler
        return render(request, "uretsatapp/sepet.html", context)

def sepetEkle(request, id):
    if not request.user.is_authenticated:
        return redirect("/giris")
    
    sepet = Siparisler.objects.filter(user=request.user, tamamlandi=False)
    if len(sepet) > 0:
        sepet[0].urunler.add(Urun.objects.get(id=id))
    else:
        sepet = Siparisler.objects.create(user=request.user, tamamlandi=False)
        sepet.urunler.add(Urun.objects.get(id=id))

    return redirect("/sepet")

def sepetSil(request, id):
    if not request.user.is_authenticated:
        return redirect("/giris")

    sepet = Siparisler.objects.get(user=request.user, tamamlandi=False)
    sepet.urunler.remove(Urun.objects.get(id=id))
    return redirect("/sepet")

def odeme(request):
    if not request.user.is_authenticated:
        return redirect("/giris")

    sepet = Siparisler.objects.get(user=request.user, tamamlandi=False)
    sepet.tamamlandi = True
    sepet.save()
    messages.success(request, "alışverişinizi tamamladınız.")
    return redirect("/siparislerim")

def siparislerim(request):
    if not request.user.is_authenticated:
        return redirect("/giris")

    siparisler_db = list(Siparisler.objects.filter(user=request.user, tamamlandi=True))
    siparisler = []
    for s in siparisler_db:
        siparis = {}
        siparis["id"] = s.id
        urunler = []
        for u in s.urunler.all():
            urun = {
                "id": u.id,
                "ad": u.ad,
                "tur": u.tur,
                "stok": u.stok,
                "fiyat": u.fiyat,
                "detay": u.detay,
                "resim": u.resim,
            }

            rate_db = Rate.objects.filter(user = request.user, urun=u)
            rate = rate_db[0].rate if rate_db else 0
            urun["rate"] = rate
            urunler.append(urun)
        siparis["urunler"] = urunler
        siparisler.append(siparis)

    context = {
        "siparisler": siparisler
    }
    return render(request, "uretsatapp/siparislerim.html", context)

def rate(request, id):
    if not request.user.is_authenticated:
        return redirect("/giris")
    
    urun = Urun.objects.get(id=id)
    degerlendirme = Rate.objects.filter(user = request.user, urun = urun)
    rate = request.POST.get("rate")

    if rate:    
        if (len(degerlendirme) == 0):
            Rate.objects.create(user = request.user, urun=urun, rate=rate)
        else:
            degerlendirme[0].rate = rate
            degerlendirme[0].save()

    return redirect("/siparislerim")
    