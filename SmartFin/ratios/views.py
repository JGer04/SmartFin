from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from app.cuentaBalance.models import *
from app.cuentaResultado.models import *
from .forms import *

# Create your views here.
# Lista de secciones
def lista_secciones(request):
    secciones = Seccion.objects.all()
    return render(request, 'ratios/lista_secciones.html', {'secciones': secciones})

# Crear sección
def crear_seccion(request):
    if request.method == 'POST':
        form = SeccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_secciones')
    else:
        form = SeccionForm()
    return render(request, 'ratios/crear_seccion.html', {'form': form})

# Editar sección
def editar_seccion(request, pk):
    seccion = get_object_or_404(Seccion, pk=pk)
    if request.method == 'POST':
        form = SeccionForm(request.POST, instance=seccion)
        if form.is_valid():
            form.save()
            return redirect('lista_secciones')
    else:
        form = SeccionForm(instance=seccion)
    return render(request, 'ratios/editar_seccion.html', {'form': form})

# Eliminar sección
def eliminar_seccion(request, pk):
    seccion = get_object_or_404(Seccion, pk=pk)
    if request.method == 'POST':
        seccion.delete()
        return redirect('lista_secciones')
    return render(request, 'ratios/eliminar_seccion.html', {'seccion': seccion})

# ratios/views.py

# Lista de subsecciones
def lista_subsecciones(request):
    subsecciones = SubSeccion.objects.all()
    return render(request, 'ratios/lista_subsecciones.html', {'subsecciones': subsecciones})

# Crear subsección
def crear_subseccion(request):
    if request.method == 'POST':
        form = SubSeccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_subsecciones')
    else:
        form = SubSeccionForm()
    return render(request, 'ratios/crear_subseccion.html', {'form': form})

# Editar subsección
def editar_subseccion(request, pk):
    subseccion = get_object_or_404(SubSeccion, pk=pk)
    if request.method == 'POST':
        form = SubSeccionForm(request.POST, instance=subseccion)
        if form.is_valid():
            form.save()
            return redirect('lista_subsecciones')
    else:
        form = SubSeccionForm(instance=subseccion)
    return render(request, 'ratios/editar_subseccion.html', {'form': form})

# Eliminar subsección
def eliminar_subseccion(request, pk):
    subseccion = get_object_or_404(SubSeccion, pk=pk)
    if request.method == 'POST':
        subseccion.delete()
        return redirect('lista_subsecciones')
    return render(request, 'ratios/eliminar_subseccion.html', {'subseccion': subseccion})

# ratios/views.py

# Lista de razones
def lista_razones(request):
    razones = Razon.objects.all()
    return render(request, 'ratios/lista_razones.html', {'razones': razones})

# Crear razón
def crear_razon(request):
    if request.method == 'POST':
        form = RazonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_razones')
    else:
        form = RazonForm()
    return render(request, 'ratios/crear_razon.html', {'form': form})

# Editar razón
def editar_razon(request, pk):
    razon = get_object_or_404(Razon, pk=pk)
    if request.method == 'POST':
        form = RazonForm(request.POST, instance=razon)
        if form.is_valid():
            form.save()
            return redirect('lista_razones')
    else:
        form = RazonForm(instance=razon)
    return render(request, 'ratios/editar_razon.html', {'form': form})

# Eliminar razón
def eliminar_razon(request, pk):
    razon = get_object_or_404(Razon, pk=pk)
    if request.method == 'POST':
        razon.delete()
        return redirect('lista_razones')
    return render(request, 'ratios/eliminar_razon.html', {'razon': razon})

def menu_cruds(request):
    balances = Balance.objects.all()  # Obtiene todos los balances
    return render(request, 'ratios/casita.html', {'balances': balances})

def calcular_ratios(request, id_balance):
    #calculo de liquidez corriente
    # Filtramos las cuentas por el año especificado
    tac = CuentaBalance.objects.get(idBalance=id_balance, codigo='tac')
    tpc = CuentaBalance.objects.get(idBalance=id_balance, codigo='tpc')

    # Verificamos que ambas cuentas existan y evitamos la división por cero
    ratio_valor = None
    if tac and tpc and tpc.monto != 0:
        ratio_valor = tac.monto / tpc.monto
        guardar = Razon.objects.get(id=1)
        guardar.valor = ratio_valor
        guardar.save()
    elif tpc and tpc.monto == 0:
        ratio_valor = "División por cero"
    else:
        ratio_valor = "Datos insuficientes para el cálculo"

    #calculo de liquidez rapida
    inv = CuentaBalance.objects.get(idBalance=id_balance, codigo='1105')
    # Verificamos que ambas cuentas existan y evitamos la división por cero
    ratio_valor = None
    if tac and tpc and tpc.monto != 0:
        ratio_valor = (tac.monto-inv.monto) / tpc.monto
        guardar = Razon.objects.get(id=2)
        guardar.valor = ratio_valor
        guardar.save()
    elif tpc and tpc.monto == 0:
        ratio_valor = "División por cero"
    else:
        ratio_valor = "Datos insuficientes para el cálculo"

    #calculo de razon de activo neto
    ta = CuentaBalance.objects.get(idBalance=id_balance, codigo='tc')
    ratio_valor = None
    if tac and ta and ta.monto != 0:
        ratio_valor = (tac.monto-tpc.monto) / ta.monto
        guardar = Razon.objects.get(id=3)
        guardar.valor = ratio_valor
        guardar.save()
    elif tpc and tpc.monto == 0:
        ratio_valor = "División por cero"
    else:
        ratio_valor = "Datos insuficientes para el cálculo"

    #calculo de razon de efectivo
    efe = CuentaBalance.objects.get(idBalance=id_balance, codigo='1101')
    ratio_valor = None
    if efe and tpc and tpc.monto != 0:
        ratio_valor = efe.monto / tpc.monto
        guardar = Razon.objects.get(id=4)
        guardar.valor = ratio_valor
        guardar.save()
    elif tpc and tpc.monto == 0:
        ratio_valor = "División por cero"
    else:
        ratio_valor = "Datos insuficientes para el cálculo"

    #calculo de razon de rotacion de inventario
    cv = CuentaResultado.objects.get(idResultado=id_balance, codigo='43')
    ratio_valor = None
    if cv and inv and inv.monto != 0 and id_balance==1:
        ratio_valor = cv.monto / inv.monto
        guardar = Razon.objects.get(id=5)
        guardar.valor = ratio_valor
        guardar.save()
    elif cv and inv and inv.monto != 0 and id_balance!=1:
        aniopas = CuentaBalance.objects.get(idBalance=id_balance-1, codigo='1105')
        ratio_valor = cv.monto / ((inv.monto+aniopas.monto)/2)
        guardar = Razon.objects.get(id=5)
        guardar.valor = ratio_valor
        guardar.save()
    elif tpc and tpc.monto == 0:
        ratio_valor = "División por cero"
    else:
        ratio_valor = "Datos insuficientes para el cálculo"

    #calculo de razon de rotacion de inventario en dias
    if  ratio_valor !=0:
        ratio_valor = 365 / ratio_valor
        guardar = Razon.objects.get(id=6)
        guardar.valor = ratio_valor
        guardar.save()
    elif tpc and tpc.monto == 0:
        ratio_valor = "División por cero"
    else:
        ratio_valor = "Datos insuficientes para el cálculo"

#calculo de razon de  de cuentas por cobrar
    vn = CuentaResultado.objects.get(idResultado=id_balance, codigo='42')
    vn1 = CuentaResultado.objects.get(idResultado=id_balance, codigo='41')
    vn.monto = vn.monto + vn1.monto
    cc = CuentaBalance.objects.get(idBalance=id_balance, codigo='1102') 
    ratio_valor = None
    if vn and cc and cc.monto != 0 and id_balance==1:
        ratio_valor = vn.monto / cc.monto
        guardar = Razon.objects.get(id=7)
        guardar.valor = ratio_valor
        guardar.save()
    elif vn and cc and cc.monto != 0 and id_balance!=1:
        aniopas = CuentaBalance.objects.get(idBalance=id_balance-1, codigo='1102')
        ratio_valor = vn.monto / ((cc.monto+aniopas.monto)/2)
        guardar = Razon.objects.get(id=7)
        guardar.valor = ratio_valor
        guardar.save()
    elif tpc and tpc.monto == 0:
        ratio_valor = "División por cero"
    else:
        ratio_valor = "Datos insuficientes para el cálculo"

 #calculo de razon de rotacion de periodo medio de cobranza en dias
    if  ratio_valor !=0:
        ratio_valor = 365 / ratio_valor
        guardar = Razon.objects.get(id=8)
        guardar.valor = ratio_valor
        guardar.save()
    elif tpc and tpc.monto == 0:
        ratio_valor = "División por cero"
    else:
        ratio_valor = "Datos insuficientes para el cálculo"

 #calculo de razon de  de cuentas por pagar
    cv = CuentaResultado.objects.get(idResultado=id_balance, codigo='43')
    cp = CuentaBalance.objects.get(idBalance=id_balance, codigo='2101')
    ratio_valor = None
    if cv and cc and inv.monto != 0 and id_balance==1:
        ratio_valor = cv.monto + inv.monto
        ratio_valor = ratio_valor/cp.monto
        guardar = Razon.objects.get(id=9)
        guardar.valor = ratio_valor
        guardar.save()
    elif vn and cc and cc.monto != 0 and id_balance!=1:
        aniopas = CuentaBalance.objects.get(idBalance=id_balance-1, codigo='1105')
        anicp = CuentaBalance.objects.get(idBalance=id_balance-1, codigo='2101')

        ratio_valor = cv.monto + (inv - aniopas)
        ratio_valor = ratio_valor/((cp.monto + anicp.monto)/2) 
        guardar = Razon.objects.get(id=9)
        guardar.valor = ratio_valor
        guardar.save()
    elif tpc and tpc.monto == 0:
        ratio_valor = "División por cero"
    else:
        ratio_valor = "Datos insuficientes para el cálculo" 
    
    #calculo de Razón de período medio de pago
    if  ratio_valor !=0:
        ratio_valor = 365 / ratio_valor
        guardar = Razon.objects.get(id=10)
        guardar.valor = ratio_valor
        guardar.save()
    elif tpc and tpc.monto == 0:
        ratio_valor = "División por cero"
    else:
        ratio_valor = "Datos insuficientes para el cálculo"

#calculo de Rotación de activos totales
    at = CuentaBalance.objects.get(idBalance=id_balance, codigo='tc')
    ratio_valor = None
    if vn and at.monto != 0 and id_balance==1:
        ratio_valor = vn.monto / at.monto
        guardar = Razon.objects.get(id=11)
        guardar.valor = ratio_valor
        guardar.save()
    elif vn and at and at.monto != 0 and id_balance!=1:
        aniopas = CuentaBalance.objects.get(idBalance=id_balance-1, codigo='tc')
        ratio_valor = vn.monto/((at.monto + aniopas.monto)/2) 
        guardar = Razon.objects.get(id=11)
        guardar.valor = ratio_valor
        guardar.save()
    elif tpc and tpc.monto == 0:
        ratio_valor = "División por cero"
    else:
        ratio_valor = "Datos insuficientes para el cálculo" 

#calculo de Rotación de activos fijos
    oa = CuentaBalance.objects.get(idBalance=id_balance, codigo='1108')
    ratio_valor = None
    if vn and at.monto != 0 and id_balance==1:
        ratio_valor = vn.monto / oa.monto
        guardar = Razon.objects.get(id=12)
        guardar.valor = ratio_valor
        guardar.save()
    elif vn and at and at.monto != 0 and id_balance!=1:
        aniopas = CuentaBalance.objects.get(idBalance=id_balance-1, codigo='1108')
        ratio_valor = vn.monto/((oa.monto + aniopas.monto)/2) 
        guardar = Razon.objects.get(id=12)
        guardar.valor = ratio_valor
        guardar.save()
    elif tpc and tpc.monto == 0:
        ratio_valor = "División por cero"
    else:
        ratio_valor = "Datos insuficientes para el cálculo" 

#calculo de margen bruto
    utb = CuentaResultado.objects.get(idResultado=id_balance, codigo='ub')
    ratio_valor = None
    if vn and utb.monto != 0 and id_balance==1:
        ratio_valor = utb.monto / vn.monto
        guardar = Razon.objects.get(id=13)
        guardar.valor = ratio_valor
        guardar.save()
    elif tpc and tpc.monto == 0:
        ratio_valor = "División por cero"
    else:
        ratio_valor = "Datos insuficientes para el cálculo" 

#calculo de margen bruto
    uo = CuentaResultado.objects.get(idResultado=id_balance, codigo='uo')
    ratio_valor = None
    if vn and uo.monto != 0 and id_balance==1:
        ratio_valor = uo.monto / vn.monto
        guardar = Razon.objects.get(id=14)
        guardar.valor = ratio_valor
        guardar.save()
    elif tpc and tpc.monto == 0:
        ratio_valor = "División por cero"
    else:
        ratio_valor = "Datos insuficientes para el cálculo" 




    razones = Razon.objects.all()
    # Pasamos el resultado al template
    context = {
        'id_balance': id_balance,
        'razones':razones
    }
    return render(request, 'ratios/resultado_ratio.html', context)