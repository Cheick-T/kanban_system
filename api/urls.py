from django.urls import path
from . import views
from django.conf.urls import url

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Archivage API",
        default_version='v1',
        description="API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ismael@timite.net"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger',
                                           cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc',
                                         cache_timeout=0), name='schema-redoc'),


    path('dossiers', views.ListDossier.as_view()),
    path('dossiers/<int:pk>', views.DetailDossier.as_view()),

    path('agents', views.ListAgent.as_view()),
    path('agents/<int:pk>', views.DetailAgent.as_view()),

    path('mouvements', views.ListMouvement.as_view()),
    path('mouvements/<int:pk>', views.DetailMouvement.as_view()),

]
