
from .models import Usuario

def usuario_context(request):
    usuario = None
    if request.session.get('usuario_id'):
        try:
            usuario = Usuario.objects.get(id=request.session['usuario_id'])
        except Usuario.DoesNotExist:
            pass
    return {'usuario': usuario}