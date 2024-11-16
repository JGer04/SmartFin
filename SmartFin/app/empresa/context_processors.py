from app.empresa.models import Empresa

def empresas_context(request):
    return {
        'empresas': Empresa.objects.all()
    }
