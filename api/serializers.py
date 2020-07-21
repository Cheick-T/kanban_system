from rest_framework import serializers
from app.models import *

GENERIC_FIELDS = ('code', 'categorie_dossier',
                  'state', 'creation_time', 'update_time')


class FolderCategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', 'description', 'active')
        model = FolderCategory


class DossierSerializer(serializers.ModelSerializer):
    categorie_dossier = FolderCategorySerializer()

    class Meta:
        fields = GENERIC_FIELDS
        model = Dossier
