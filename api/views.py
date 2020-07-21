from rest_framework import generics

from app.models import *
from .serializers import *


class ListDossier(generics.ListCreateAPIView):
    queryset = Dossier.objects.all()
    serializer_class = DossierSerializer


class DetailDossier(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dossier.objects.all()
    serializer_class = DossierSerializer
