from django.conf.urls import url
from django.urls import path
from django.contrib import admin

# , valider_mouvement, valider_in, , OutMouvement
from app.views import InMouvement, OutMouvement

urlpatterns = [
    # url(r'^valider_mouvement/(?P<dossier_id>\d+)/(?P<next_state_id>\d+)/$',
    #    valider_mouvement, name='valider_mouvement'),
    # url(r'^validate_in/(?P<dossier_id>\d+)/(?P<next_state_id>\d+)/(?P<emplacement_id>\d+)$',
    #    InMouvement.as_view(), name='validate_in'),
    # url(r'^validate_out/(?P<dossier_id>\d+)/(?P<next_state_id>\d+)/(?P<agent_id>\d+)$',
    #    OutMouvement.as_view(), name='validate_out'),
    url(r'^validate_in/(?P<dossier_id>\d+)/(?P<next_state_id>\d+)/$',
        InMouvement.as_view(), name='validate_in'),
    url(r'^validate_out/(?P<dossier_id>\d+)/(?P<next_state_id>\d+)/$',
        OutMouvement.as_view(), name='validate_out'),
    
]
