from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Marka, Seri, Model, VitesTipi, KasaTipi, YakıtTipi, Çekiş
from .forms import AracForm
from models.data_preprocessing import preprocess_data, main
from django.contrib.auth import authenticate, logout
from .models import Arac
def form_page(request):
    if request.method == 'POST':
        form = AracForm(request.POST)
        if form.is_valid():
            arac=form.save(commit=False)
            arac.author= request.user
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
    context= {'predicted_price': predict_value}
    
    return render(request, 'priceForm/success.html', context)

def car_info(request):
    # Sayfa yüklendiğinde, tüm markaları göstermek için kullanılabilir.
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
