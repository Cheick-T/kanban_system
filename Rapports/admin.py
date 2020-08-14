from django.contrib import admin
from app.models import * 
from app.admin import DossierAdmin,MouvementAdmin


# Register your models here.

class DossierOut(Dossier):
    class Meta:
        proxy = True
        verbose_name_plural = "Rapport - Liste des dossiers out"

class DossierOutAdmin(DossierAdmin):
    list_display = ['categorie_dossier', 'code', 'location', 'out_since']
    list_per_page=10
    def get_queryset(self, request):
        return self.model.objects.filter(state__description='out')

    def has_add_permission(self, request, obj=None):
        return False

class RapportMouvement(Mouvement):
    class Meta:
        proxy = True

class Mouvement1Admin(MouvementAdmin):
    def get_queryset(self, request):
        return self.model.objects.all()


admin.site.register(DossierOut, DossierOutAdmin)
admin.site.register(RapportMouvement, Mouvement1Admin)
