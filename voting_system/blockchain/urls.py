from django.urls import path
from . import views

urlpatterns = [
    path('mine/', views.mine, name='mine'),
    path('vote/', views.vote, name='vote'),
    path('chain/', views.full_chain, name='full_chain'),
    path('votes/', views.votes, name='votes'),
]
