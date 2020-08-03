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


class AgentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', 'description', 'active')
        model = AgentCategory


class AgentSerializer(serializers.ModelSerializer):
    categorie_agent = AgentCategorySerializer()

    class Meta:
        fields = ('code','nom','prenoms','categorie_agent')
        model = Agent

class EmplacementMPTTSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'parent')
        model = EmplacementMPTT

class MouvementSerializer(serializers.ModelSerializer):
    dossier = DossierSerializer()
    agent = AgentSerializer()
    emplacement= EmplacementMPTTSerializer()

    class Meta:
        fields = ('dossier','agent','emplacement','sens')
        model = Mouvement

