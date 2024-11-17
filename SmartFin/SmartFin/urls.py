from django.contrib.auth import logout, get_user_model, authenticate, login
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required

#Para renderizar la página de inicio
@login_required
def index(request):
    return render(request, 'home.html')

def exit(request):
    logout(request)
    return redirect('login')

@login_required
def menu_comparativo(request):
    return render(request, 'menu_comparativo.html')

@login_required
def menu_individual(request):
    return render(request, 'menu_individual.html')

urlpatterns = [
    path('', index, name='index'),
    #path('login/', login_v, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', exit, name='exit'),
    path('analisis-menu-comparativo', menu_comparativo, name = 'menu_comparativo'),
    path('analisis-menu-individual', menu_individual, name = 'menu_individual'),
    path('admin/', admin.site.urls),

    path('', include ('app.balance.urls')),
    path('', include ('app.cuentaBalance.urls')),
    path('', include ('app.cuentaResultado.urls')),
    path('', include ('app.empresa.urls')),
    path('', include ('app.resultado.urls')),
    path('', include ('app.usuario.urls')),
    path('ratios/', include ('ratios.urls')),
    
]
