from django.contrib import admin
from .models import *
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from reversion.admin import VersionAdmin


from django.urls import reverse
from django.utils.safestring import mark_safe


admin.site.site_header = 'Archivage des dossiers'

admin.site.site_title = 'Archivage des dossiers'
admin.site.index_title = "Espace d'administration"


def create_actions_buttons(obj, transition_approval):
    # approbation_url = reverse('valider_mouvement', kwargs={
    #                          'dossier_id': obj.pk, 'next_state_id': transition_approval.transition.destination_state.pk})

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


class BaseApplicationAdmin(VersionAdmin):
    date_hierarchy = 'update_time'
    readonly_fields = ['update_time', 'creation_time']


class MouvementAdmin(BaseApplicationAdmin):
    list_display = ['dossier', 'agent',
                    'emplacement', 'creation_time', ]
    search_fields = ['dossier__code']
    list_filter = ['agent', 'creation_time', ]
    list_select_related = ('dossier', 'agent', 'emplacement',)


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


class MouvementCreationInline(admin.TabularInline):
    model = Mouvement
    max_num = 1
    fields = ['dossier', 'emplacement', ]
    verbose_name = "Emplacement initial"
    verbose_name_plural = "Emplacement initial"


class DossierAdmin(BaseApplicationAdmin):
    list_display = ['categorie_dossier', 'code', 'location',
                    'state', 'actions_buttons']
    list_display_links = ['categorie_dossier', 'code', ]
    search_fields = ['code']
    list_filter = ['categorie_dossier__title', 'state', 'creation_time', ]
    list_select_related = ('categorie_dossier', )

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
        # if obj.state.description == "in":
        #    ancetres = ' > '.join(
        #        [x.name for x in obj.emplacement.get_ancestors()])
        #    return ancetres + " > " + obj.emplacement.name
        # else:
        #    return obj.mouvements.latest('creation_time').agent

        if obj.state.description == "in":

            ancetres = ' > '.join(
                [x.name for x in obj.mouvements.filter(sens="in").latest('creation_time').emplacement.get_ancestors()])
            print(ancetres)
            print(type(obj.mouvements.filter(sens="in").latest(
                'creation_time').emplacement))
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


class EmplacementAdmin(TreeAdmin, BaseApplicationAdmin):
    form = movenodeform_factory(Emplacement)


# Register your models here.
admin.site.register(AgentCategory)
admin.site.register(FolderCategory)
admin.site.register(Agent)
admin.site.register(Dossier, DossierAdmin)
admin.site.register(Emplacement, EmplacementAdmin)
admin.site.register(Mouvement, MouvementAdmin)
