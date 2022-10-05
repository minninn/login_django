from django.urls import path
from . import views

urlpatterns = [
    path( '', views.login ),
    path( 'signup/', views.signup ),
    path( 'logout/', views.logout ),
    path( 'ctf/', views.ctf ),
    path( 'mypage/', views.mypage ),
    path( 'aevkajhefhwo34paw89r1v2o95uqw98r3/', views.resign ),
]