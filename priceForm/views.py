from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Marka, Seri, Model, VitesTipi, KasaTipi, YakıtTipi, Çekiş
from .forms import AracForm
from models.data_preprocessing import main
from django.contrib.auth import authenticate, logout
from .models import Arac
def form_page(request):
    if request.method == 'POST':
        form = AracForm(request.POST)
        if form.is_valid():
            arac=form.save(commit=False)
            arac.author= request.user
            arac.save()
            predict_value=main()
            arac.TahminiFiyat = predict_value
            arac.save()
            return redirect('priceForm:success') 
    else:
        form = AracForm()

    markalar = Marka.objects.all()
    seriler = Seri.objects.all()
    modeller = Model.objects.all()
    vites_tipleri = VitesTipi.objects.all()
    kasalar = KasaTipi.objects.all()
    yakit_tipleri = YakıtTipi.objects.all()
    çekiş_tipi = Çekiş.objects.all()

    return render(request, "priceForm/form_page.html", {
        'form': form,
        'markalar': markalar,
        'seriler': seriler,
        'modeller': modeller,
        'vites_tipleri': vites_tipleri,
        'kasa_tipleri': kasalar,
        'yakit_tipleri': yakit_tipleri,
        'çekiş_tipleri': çekiş_tipi,
    })

def success(request):
    predict_value=main()
    tam_sayi=int(predict_value)
    sayi_str = str(tam_sayi)
    basamaklar = [int(digit) for digit in sayi_str]
    if len(basamaklar) == 6:
        yeni_string = f'{basamaklar[0]}{basamaklar[1]}{basamaklar[2]}.{basamaklar[3]}{basamaklar[4]}{basamaklar[5]}'
        fixed_value=yeni_string
    elif len(basamaklar)== 7:
        yeni_string = f'{basamaklar[0]}.{basamaklar[1]}{basamaklar[2]}{basamaklar[3]}.{basamaklar[4]}{basamaklar[5]}{basamaklar[6]}'
        fixed_value=yeni_string
    elif len(basamaklar)==8:
        yeni_string = f'{basamaklar[0]}{basamaklar[1]}.{basamaklar[2]}{basamaklar[3]}{basamaklar[4]}.{basamaklar[5]}{basamaklar[6]}{basamaklar[7]}'
        fixed_value=yeni_string
    elif len(basamaklar)==9:
        yeni_string = f'{basamaklar[0]}{basamaklar[1]}{basamaklar[2]}.{basamaklar[3]}{basamaklar[4]}{basamaklar[5]}.{basamaklar[6]}{basamaklar[7]}{basamaklar[8]}'
        fixed_value=yeni_string
    elif len(basamaklar)==5:
        yeni_string = f'{basamaklar[0]}{basamaklar[1]}.{basamaklar[2]}{basamaklar[3]}{basamaklar[4]}'
        fixed_value=yeni_string
    context= {'predicted_price': fixed_value}
    
    return render(request, 'priceForm/success.html', context)

def car_info(request):
    markalar = Marka.objects.all()
    return render(request, 'form_page.html', {'markalar': markalar})

def get_marka_suggestions(request):
    marka = request.GET.get('marka', '')
    markalar = Marka.objects.filter(isim__icontains=marka).values_list('isim', flat=True)
    suggestions = list(markalar)
    return JsonResponse({'marka_suggestions': suggestions})

def get_seri_suggestions(request):
    seri = request.GET.get('seri', '')
    seriler = Seri.objects.filter(seri_adi__icontains=seri).values_list('seri_adi', flat=True)
    suggestions = list(seriler)
    return JsonResponse({'seri_suggestions': suggestions})

def get_model_suggestions(request):
    model = request.GET.get('model', '')
    modeller = Model.objects.filter(model_adi__icontains=model).values_list('model_adi', flat=True)
    suggestions = list(modeller)
    return JsonResponse({'model_suggestions': suggestions})

def previous(request):
    user = request.user
    user_cars = Arac.objects.filter(author=user)
    
    context = {
        'user_cars': user_cars
    }
    return render(request, 'priceForm/previous.html', context)
