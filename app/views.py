from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.urls import reverse, reverse_lazy
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from river.models import State
from app.models import Dossier, Mouvement, Agent#, Emplacement

from .forms import InForm, OutForm
from django.views.generic.edit import CreateView

# TODO : handle transactions



class InMouvement(CreateView):
    form_class = InForm
    model = Mouvement
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('admin:app_dossier_changelist')

    def get_initial(self, *args, **kwargs):
        return {
            "dossier": get_object_or_404(Dossier, pk=self.kwargs.get('dossier_id')),
        }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            self.object.save()
            try:
                dossier = get_object_or_404(
                Dossier, pk=self.kwargs.get('dossier_id'))
                next_state = get_object_or_404(
                State, pk=self.kwargs.get('next_state_id'))

                dossier.river.state.approve(
                    as_user=self.request.user, next_state=next_state)

                messages.success(self.request, mark_safe('Operation effectuée avec succès : "<b>{}</b>" remis à "<b>{}</b>"'.format(dossier, self.object.emplacement)))
                

            except :
                self.object.delete()
                messages.success(self.request, "Rollback effectué: erreur durant la mise à jour du statut du dossier")
        except:
            messages.success(self.request, "Erreur : echec de creation du mouvement")
            #print("An exception occurred while saving mouvemnt")



        # TODO: et en cas de problème pour changer l'état, supprimer l'object Mouvement précédemment créé
        return HttpResponseRedirect(self.get_success_url())


class OutMouvement(CreateView):
    form_class = OutForm
    model = Mouvement
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('admin:app_dossier_changelist')

    def get_initial(self, *args, **kwargs):
        return {
            "dossier": get_object_or_404(Dossier, pk=self.kwargs.get('dossier_id')),
        }

    def form_valid(self, form):
        self.object = form.save(commit=False)

        try :
            self.object.save()

            try:

                dossier = get_object_or_404(
                    Dossier, pk=self.kwargs.get('dossier_id'))
                next_state = get_object_or_404(
                    State, pk=self.kwargs.get('next_state_id'))

                dossier.river.state.approve(
                    as_user=self.request.user, next_state=next_state)

                #messages.success(request, f"Modification approuvée pour le dossier: {dossier}")
                messages.success(self.request, mark_safe('Operation effectuée avec succès : "<b>{}</b>" remis à "<b>{}</b>"'.format(dossier, self.object.agent)))
                # TODO: et en cas de problème pour changer l'état, supprimer l'object Mouvement précédemment créé
                
            except:
                messages.success(self.request, "Rollback effectué: erreur durant la mise à jour du statut du dossier")
                self.object.delete()
        except:
            #print("error mouvement")
            messages.success(self.request, "Erreur : echec de creation du mouvement")

        return HttpResponseRedirect(self.get_success_url())  

