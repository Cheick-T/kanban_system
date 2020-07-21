from django.db import models
from treebeard.mp_tree import MP_Node
from river.models.fields.state import StateField


class TimedModel(models.Model):

    creation_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AgentCategory(TimedModel):
    title = models.CharField(max_length=50, blank=False)
    description = models.CharField(
        'Description', max_length=200, blank=True, null=True)
    active = models.BooleanField('Active', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Catégorie d'agents"
        verbose_name_plural = "Catégories d'agents"
        ordering = ['title']


class FolderCategory(TimedModel):
    title = models.CharField(max_length=50, blank=False)
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
    code = models.CharField(max_length=10, blank=False)
    nom = models.CharField(max_length=50, blank=False)
    prenoms = models.CharField(max_length=50, blank=True, null=True)
    categorie_agent = models.ForeignKey(
        "AgentCategory", on_delete=models.PROTECT, related_name="agents", limit_choices_to={'active': True})

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
    code = models.CharField(max_length=10, blank=False)
    categorie_dossier = models.ForeignKey(
        "FolderCategory", on_delete=models.PROTECT, related_name="dossiers")
    # emplacement = models.ForeignKey(
    #    "Emplacement", on_delete=models.PROTECT, related_name="dossiers")
    state = StateField(editable=False)

    def __str__(self):
        return "{} / {}".format(self.categorie_dossier, self.code)

    class Meta:
        verbose_name = "Dossier"
        verbose_name_plural = "Dossiers"
        permissions = [
            ("can_manipulate_folders", "Can manipulate folders"),
        ]


class Emplacement(TimedModel, MP_Node):
    name = models.CharField(max_length=30)

    node_order_by = ['name']

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = "Emplacement de dossiers"
        verbose_name_plural = "Emplacements de dossiers"


class Mouvement(TimedModel):

    dossier = models.ForeignKey(
        "Dossier", on_delete=models.PROTECT, related_name="mouvements")
    agent = models.ForeignKey(
        "Agent", on_delete=models.SET_NULL, null=True, related_name="mouvements")
    emplacement = models.ForeignKey("Emplacement", on_delete=models.SET_NULL, null=True,
                                    related_name="mouvements")
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
        verbose_name_plural = "Mouvements de dossiers"
        ordering = ['dossier', 'creation_time', ]
