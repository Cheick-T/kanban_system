from django.contrib import admin, messages
from .models import *
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from mptt.admin import DraggableMPTTAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from reversion.admin import VersionAdmin
from django.db.models import F

from django.db.models import Count
from django.db.models.functions import TruncDay
import json
from django.core.serializers.json import DjangoJSONEncoder

from django.urls import reverse
from django.utils.safestring import mark_safe


admin.site.site_header = 'Archivage des dossiers'
admin.site.site_title = 'Archivage des dossiers'
admin.site.index_title = "Espace d'administration"


def create_actions_buttons(obj, transition_approval):
    sens_mouvement = transition_approval.transition.destination_state.description

    if sens_mouvement == 'in':
        approbation_url = reverse('validate_in', kwargs={
            'dossier_id': obj.pk,
            # 'emplacement_id': obj.emplacement.pk,
            'next_state_id': transition_approval.transition.destination_state.pk})

    if sens_mouvement == 'out':
        approbation_url = reverse('validate_out', kwargs={
            'dossier_id': obj.pk,
            # 'agent_id': obj.emplacement.pk,
            'next_state_id': transition_approval.transition.destination_state.pk})

    return f"""
		<input
			type="button"
			style="margin:2px;2px;2px;2px;"
			value="{transition_approval.transition.source_state} -> {transition_approval.transition.destination_state}"
			onclick="location.href=\'{approbation_url}\'"
		/>
	"""


class DansSalleArchivageFilter(admin.SimpleListFilter):
    title = 'presence_salle_archivage'
    parameter_name = 'is_in_archive'
    
    def lookups(self, request, model_admin):
        return (
            ('Oui', 'Oui'),
            ('Non', 'Non'),
        )
    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Oui':
            return queryset.filter(state__description="in")
        elif value == 'Non':
            return queryset.exclude(state__description="in")
        return queryset

class BaseApplicationAdmin(VersionAdmin,admin.ModelAdmin):
    date_hierarchy = 'update_time'
    readonly_fields = ['update_time', 'creation_time']


class MouvementAdmin(admin.ModelAdmin):
    list_display = ['dossier', 'agent',
                    'emplacement', 'creation_time',]#'timeout' ]
    search_fields = ['dossier__code']
    list_filter = ['agent', 'creation_time', ]
    list_select_related = ('dossier', 'agent', 'emplacement',)
    readonly_fields = ['sens', 'dossier', 'agent',
                       'emplacement', 'update_time', 'creation_time']
    list_per_page=10

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

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


class MouvementInline(admin.TabularInline):
    model = Mouvement
    extra = 0
    fields = ['dossier', 'agent', 'emplacement', 'creation_time']
    readonly_fields = ['dossier', 'agent', 'emplacement', 'creation_time']

    verbose_name = "Historique de mouvements de dossiers"
    verbose_name_plural = "Historique de mouvements de dossiers"

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False



class MouvementCreationInline(admin.TabularInline):
    model = Mouvement
    max_num = 1
    fields = ['dossier', 'emplacement', ]
    verbose_name = "Emplacement initial"
    verbose_name_plural = "Emplacement initial"


class DossierAdmin(BaseApplicationAdmin):
    def nombre_total_de_mouvements(self):
        return len(self.mouvements.all())
        
    list_display = ['is_in_archive','categorie_dossier', 'code', 'location',
                    'state', 'actions_buttons',nombre_total_de_mouvements]
    list_display_links = ['categorie_dossier', 'code', ]
    search_fields = ['code']
    list_filter = ['categorie_dossier__title', DansSalleArchivageFilter, 'state', 'creation_time']
    list_select_related = ('categorie_dossier', )
    list_per_page=10

    def is_in_archive(self, obj):
        return obj.state.description == "in"
    is_in_archive.boolean = True

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['categorie_dossier', 'code',
                    'update_time', 'creation_time']
        else:
            return []

    def get_inlines(self, request, obj=None):
        if obj:
            return [MouvementInline, ]
        else:
            return [MouvementCreationInline, ]

    def get_list_display(self, request):
        self.user = request.user
        return super(DossierAdmin, self).get_list_display(request)

    def location(self, obj):
        if obj.state.description == "in":
            ancetres = ' > '.join(
                [x.name for x in obj.mouvements.filter(sens="in").latest('creation_time').emplacement.get_ancestors()])
            return ancetres + " > " + obj.mouvements.filter(sens="in").latest('creation_time').emplacement.name
        else:
            return obj.mouvements.filter(sens="out").latest('creation_time').agent
    
    def actions_buttons(self, obj):
        content = ""
        for transition_approval in obj.river.state.get_available_approvals(as_user=self.user):
            content += create_actions_buttons(obj, transition_approval)
        return mark_safe(content)

    def has_add_permission(self, request, obj=None):
        if obj:
            return False
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    # def get_queryset(self, request):
    #     qs = super(DossierAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     inter=qs.filter(state__description="out").filter(mouvements__agent__user__username=request.user.username).values("mouvements__agent__nom","code")
    #     code=[]
    #     for i in inter:
    #         if list(Dossier.objects.filter(code=i["code"]).values("mouvements__agent__user__username").latest('mouvements__creation_time').values())[0]==request.user.username:
    #             code.append(i["code"])
    #     #print(code)
    #     return qs.filter(code__in=code)


class EmplacementMPTTAdmin(DraggableMPTTAdmin, VersionAdmin,admin.ModelAdmin):
    mptt_level_indent = 20
    list_display = ['tree_actions', 'indented_title', ]
    list_display_links = ['indented_title', ]
    readonly_fields = ['update_time', 'creation_time']
"""
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
"""

class AgentAdmin(VersionAdmin,admin.ModelAdmin):
    def compte_dossiers_out(self):
        return len(self.mouvements.filter(dossier__state__description='out'))
    compte_dossiers_out.short_description ="Dossiers empruntés"
    
    list_display = ['categorie_agent','code',
                        'nom' ,'prenoms',compte_dossiers_out]


class AgentInline(admin.TabularInline):
    model = Agent
    readonly_fields = ['code', 
            'nom','prenoms']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

class AgentCategoryAdmin(VersionAdmin,admin.ModelAdmin):
    inlines = [AgentInline,]

"""
class DossierOutuser(Dossier):
    class Meta:
        proxy = True
        verbose_name_plural = "Dossiers Chez moi"

class DossierOutuserAdmin(DossierAdmin):
    list_display = ['categorie_dossier', 'code', 'location', 'out_since']
    list_per_page=10

    def get_queryset(self, request):
        print(request.user.username)
        return self.model.objects.filter(mouvements__agent__code=request.user.username)

    def has_add_permission(self, request, obj=None):
        return False
"""


admin.site.register(AgentCategory,AgentCategoryAdmin)
admin.site.register(FolderCategory)
admin.site.register(Agent,AgentAdmin)
admin.site.register(Dossier, DossierAdmin)
admin.site.register(EmplacementMPTT, EmplacementMPTTAdmin)

