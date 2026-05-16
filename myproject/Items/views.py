from rest_framework import viewsets, generics
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('-itemID')
    serializer_class = ItemSerializer

class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all().order_by('-itemID')
    serializer_class = ItemSerializer
