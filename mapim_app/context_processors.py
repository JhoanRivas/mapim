
from .models import Usuario

def usuario_context(request):
    if request.session.get('usuario_id'):
        usuario = Usuario.objects.get(id=request.session.get('usuario_id'))
        return {'usuario': usuario}
    return {}