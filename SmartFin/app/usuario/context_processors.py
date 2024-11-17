from app.usuario.models import AccesoUsuario

def acceso_usuarios_context(request):
    if request.user.is_authenticated:
        acceso = AccesoUsuario.objects.get(id_usuario=request.user)
    else:
        acceso = None 

    return {
        'acceso': acceso
    }