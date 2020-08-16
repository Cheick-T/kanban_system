from django.contrib import admin
from app.models import * 
from app.admin import DossierAdmin,MouvementAdmin

from django.db.models import Count
from django.db.models.functions import TruncDay
import json
from django.core.serializers.json import DjangoJSONEncoder

# Register your models here.

class DossierOut(Dossier):
    class Meta:
        proxy = True
        verbose_name_plural = "Dossiers hors de la salle d’archivage"

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
        verbose_name_plural = "Mouvements de dossiers"

class Mouvement1Admin(MouvementAdmin):
    def get_queryset(self, request):
        return self.model.objects.all()

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data_in = (
            Mouvement.objects.filter(sens = "in").annotate(date=TruncDay("creation_time"))
            .values("date")
            .annotate(y=Count("sens"))
            .order_by("-date")
        )

        chart_data_out = (
            Mouvement.objects.filter(sens = "out").annotate(date=TruncDay("creation_time"))
            .values("date")
            .annotate(y=Count("sens"))
            .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json_in = json.dumps(list(chart_data_in), cls=DjangoJSONEncoder)
        as_json_out = json.dumps(list(chart_data_out), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data_in": as_json_in, "chart_data_out":as_json_out}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(DossierOut, DossierOutAdmin)
admin.site.register(RapportMouvement, Mouvement1Admin)
