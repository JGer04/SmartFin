from django.shortcuts import render
from app.balance.models import Balance
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from app.balance.forms import BalanceForm
# Create your views here.

class listaBalance(ListView):
    model = Balance
    template_name = 'balance/lista.html'
    context_object_name = 'balances'

class crearBalance(CreateView):
    model = Balance
    form_class = BalanceForm
    template_name = 'balance/crear.html'
    success_url = reverse_lazy('lista_balance')

    def form_valid(self, form):
        messages.success(self.request, "Balance creado exitosamente.")
        return super().form_valid(form)
    
class editarBalance(UpdateView):
    model = Balance
    form_class = BalanceForm
    template_name = 'balance/editar.html'
    success_url = reverse_lazy('lista_balance')

    def form_valid(self, form):
        messages.success(self.request, "Balance editado exitosamente.")
        return super().form_valid(form)
    
class eliminarBalance(DeleteView):
    template_name = 'balance/eliminar.html'
    model = Balance
    fields = ['nombre','idEmpresa','fecha']
    success_url = reverse_lazy('lista_balance')

    def form_valid(self, form):
        messages.success(self.request,"Balance eliminado exitosamente.")
        return super().form_valid(form)
    
