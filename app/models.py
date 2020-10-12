from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from treebeard.mp_tree import MP_Node
from river.models.fields.state import StateField
from mptt.forms import TreeNodeChoiceField
from datetime import datetime, timezone
from django.utils.timesince import timesince
from django.contrib.auth.models import User

class TimedModel(models.Model):

    creation_time = models.DateTimeField(auto_now_add=True, verbose_name="Date de creation")
    update_time = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    class Meta:
        abstract = True


class AgentCategory(TimedModel):
    title = models.CharField(max_length=50, blank=False, verbose_name="Libelle")
    description = models.CharField(
        'Correspondance sur Slug de state', max_length=200, blank=True, null=True)
    active = models.BooleanField('Active', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Catégorie d'agents"
        verbose_name_plural = "Catégories d'agents"
        ordering = ['title']


class FolderCategory(TimedModel):
    title = models.CharField(max_length=50, blank=False, verbose_name="Libelle")
    description = models.CharField(
        'Description', max_length=200, blank=True, null=True)
    active = models.BooleanField('Active', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Catégorie de dossiers"
        verbose_name_plural = "Catégories de dossiers"
        ordering = ['title']


class Agent(TimedModel):
    code = models.CharField(max_length=10, blank=False) #,verbose_name="Code agent")
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    nom = models.CharField(max_length=50, blank=False, verbose_name="NOM")
    prenoms = models.CharField(max_length=50, blank=True, null=True, verbose_name="Prénoms")
    categorie_agent = models.ForeignKey(
        "AgentCategory", on_delete=models.PROTECT, related_name="agents", limit_choices_to={'active': True}, verbose_name="Catégorie")

    @property
    def fullname(self):
        return "{} {}".format(self.prenoms, self.nom.upper())

    def __str__(self):
        return "{} / {} {}".format(self.categorie_agent, self.prenoms, self.nom.upper())

    class Meta:
        verbose_name = "Agent"
        verbose_name_plural = "Agents"
        ordering = ['code', 'nom', ]


class Dossier(TimedModel):
    code = models.CharField(max_length=10, blank=False, verbose_name="Code du dossier")
    categorie_dossier = models.ForeignKey(
        "FolderCategory", on_delete=models.PROTECT, related_name="dossiers", verbose_name="Catégorie de dossier")
    state = StateField(editable=False)

    @property
    def out_since(self):
        return timesince(self.mouvements.filter(sens='out').latest('creation_time').creation_time)

    @property
    def out_since(self):
        return timesince(self.mouvements.filter(sens='out').latest('creation_time').creation_time)


    def __str__(self):
        return "{} / {}".format(self.categorie_dossier, self.code)

    class Meta:
        verbose_name = "Dossier"
        verbose_name_plural = "Dossiers"
        permissions = [
            ("can_manipulate_folders", "Can manipulate folders"),
        ]

class EmplacementMPTT(TimedModel, MPTTModel):
    name = models.CharField(max_length=30, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "Emplacement de dossiers"
        verbose_name_plural = "Emplacements de dossiers"
    
    def __str__(self):
        return "{}".format(self.name)


class Mouvement(TimedModel):

    dossier = models.ForeignKey(
        "Dossier", on_delete=models.PROTECT, related_name="mouvements")
    agent = models.ForeignKey(
        "Agent", on_delete=models.PROTECT, null=True, related_name="mouvements")
    emplacement = TreeForeignKey("EmplacementMPTT", on_delete=models.PROTECT, null=True,
                                    related_name="mouvements",)
    sens = models.CharField("Sens", max_length=3, blank=True)

    def save(self, *args, **kwargs):
        if self.agent:
            self.sens = "out"
        else:
            self.sens = "in"
        super(Mouvement, self).save(*args, **kwargs)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "Mouvement de dossier"
        verbose_name_plural = "Mouvements des dossiers"
        ordering = ['dossier', '-creation_time', ]
