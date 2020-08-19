from django.conf.urls import url
from django.urls import path

from app.views import InMouvement, OutMouvement

urlpatterns = [
    url(r'^validate_in/(?P<dossier_id>\d+)/(?P<next_state_id>\d+)/$',
        InMouvement.as_view(), name='validate_in'),
    url(r'^validate_out/(?P<dossier_id>\d+)/(?P<next_state_id>\d+)/$',
        OutMouvement.as_view(), name='validate_out'),   
]
