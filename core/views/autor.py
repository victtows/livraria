from rest_framework.viewsets import ModelViewSet

from core.models import Categoria, Autor
from core.serializers import CategoriaSerializer, AutorSerializer

class AutorViewSet(ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer