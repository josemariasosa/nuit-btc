from django.shortcuts import render, get_object_or_404
from .forms import MnemonicForm


def start_index(request):
    context = {}
    return render(request, 'wallet/setup/start.html', context)

def create_mnemonics(request):
    if request.method == 'POST':
        mnemonic_form = MnemonicForm(data=request.POST)
        if mnemonic_form.is_valid():
            pass
    else:
        mnemonic_form = MnemonicForm()
    context = {'mnemonic_form': mnemonic_form}
    return render(request, 'wallet/setup/create_mnemonics.html', context)

def load_mnemonics(request):
    context = {}
    return render(request, 'wallet/setup/load_mnemonics.html', context)
    
#    <a href="{% url "wallet:create_mnemonics" %}">1. Crear una llave nueva.</a>
#    <a href="{% url "wallet:load_mnemonics" %}">2. Cargar mis palabras mnemonicas.</a>

# Create your views here.
