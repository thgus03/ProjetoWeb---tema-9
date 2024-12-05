from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.profile, name='profile'),
    path('produto/<int:id>', views.produto, name='produto'),
    path('produto/<int:produto_id>/avaliar/', views.adicionar_review, name='adicionar_review'),
]
