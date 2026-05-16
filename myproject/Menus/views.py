from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Menu
from .serializers import MenuSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all().order_by('-id')
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]
