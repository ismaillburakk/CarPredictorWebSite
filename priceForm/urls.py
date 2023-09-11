from django.urls import path, re_path
from . import views
from django.contrib.auth.views import LogoutView

app_name='priceForm'
urlpatterns=[
    path('form/', views.form_page, name="form"),
    path('success/', views.success, name='success'),
    path('api/get_marka_suggestions/', views.get_marka_suggestions, name='get_marka_suggestions'),
    path('api/get_seri_suggestions/', views.get_seri_suggestions, name='get_seri_suggestions'),
    path('api/get_model_suggestions/', views.get_model_suggestions, name='get_model_suggestions'),
    path("previous/", views.previous, name="previous"),
]
