from django.urls import path
from . import views

app_name = 'lattes'
urlpatterns=[
    path("producoes", views.producoes, name="producoes"),
    path("perfilProducao", views.perfilProducao, name="perfilProducao"),
    path("pessoas", views.pessoas, name="pessoas"),
    path("sair", views.logout_view, name="logout"),
    path("projetos", views.projetos, name="projetos")
]