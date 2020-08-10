from django.shortcuts import render
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

                #messages.success(request, f"Modification approuvée pour le dossier: {dossier}")

                return HttpResponseRedirect(self.get_success_url())

            except :
                self.object.delete()

        except:
            print("An exception occurred while saving mouvemnt")



        # TODO: et en cas de problème pour changer l'état, supprimer l'object Mouvement précédemment créé
        


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

                # TODO: et en cas de problème pour changer l'état, supprimer l'object Mouvement précédemment créé
                return HttpResponseRedirect(self.get_success_url())
            except:
                self.object.delete()
        except:
            print("error mouvement")
          


"""
class InMouvement(CreateView):
    form_class = InForm
    model = Mouvement
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('admin:app_dossier_changelist')

    def get_initial(self, *args, **kwargs):
        return {
            "dossier": get_object_or_404(Dossier, pk=self.kwargs.get('dossier_id')),
            # "user": self.request.user
        }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        # Changer l'etat

        dossier = get_object_or_404(
            Dossier, pk=self.kwargs.get('dossier_id'))
        next_state = get_object_or_404(
            State, pk=self.kwargs.get('next_state_id'))

        self.object.dossier.river.state.approve(
            as_user=self.request.user, next_state=next_state)

        dossier.emplacement = self.object.emplacement
        dossier.save()
        # TODO: et en cas de problème pour changer l'état, supprimer l'object Mouvement précédemment créé

        #self.object.dossier = Dossier.objects.get(self.kwargs['dossier_id'])
        # self.object.agent = Emplacement.objects.get(
        #    self.kwargs['agent_id'])
        # self.object.emplacement = Emplacement.objects.get(
        #    self.kwargs['emplacement_id'])

        return HttpResponseRedirect(self.get_success_url())


class OutMouvement(CreateView):
    form_class = OutForm
    model = Mouvement
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('admin:app_dossier_changelist')

    def get_initial(self, *args, **kwargs):
        return {
            "dossier": get_object_or_404(Dossier, pk=self.kwargs.get('dossier_id')),
            "user": self.request.user
        }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        dossier = get_object_or_404(
            Dossier, pk=self.kwargs.get('dossier_id'))
        next_state = get_object_or_404(
            State, pk=self.kwargs.get('next_state_id'))

        self.object.dossier.river.state.approve(
            as_user=self.request.user, next_state=next_state)

        dossier.emplacement = None
        dossier.save()

        # TODO: et en cas de problème pour changer l'état, supprimer l'object Mouvement précédemment créé
        return HttpResponseRedirect(self.get_success_url())
"""


"""
class OutMouvement(CreateView):
    form_class = OutForm
    success_url = redirect(reverse('admin:app_dossier_changelist'))


def valider_mouvement(request, dossier_id, next_state_id=None):
    dossier = get_object_or_404(Dossier, pk=dossier_id)
    next_state = get_object_or_404(State, pk=next_state_id)

    try:
        dossier.river.state.approve(
            as_user=request.user, next_state=next_state)
        return redirect(reverse('admin:app_dossier_changelist'))
    except Exception as e:
        return HttpResponse(e.message)


def valider_in(request, dossier_id, emplacement_id, next_state_id=None):
    dossier = get_object_or_404(Dossier, pk=dossier_id)
    emplacement = get_object_or_404(Emplacement, pk=emplacement_id)
    next_state = get_object_or_404(State, pk=next_state_id)

    try:
        # Créer le mouvement
       # Mouvement.
        # Puis, changer le statut du dossier
        dossier.river.state.approve(
            as_user=request.user, next_state=next_state)

        return redirect(reverse('admin:app_dossier_changelist'))
    except Exception as e:
        return HttpResponse(e.message)
"""
