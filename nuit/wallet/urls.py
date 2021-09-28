from django.urls import path
from . import views

app_name = 'wallet'
urlpatterns = [
    path('start/', views.start_index, name='start_index'),
    path('create-mnemonic/', views.create_mnemonics, name='create_mnemonics'),
    path('load-mnemonic/', views.load_mnemonics, name='load_mnemonics'),
]
