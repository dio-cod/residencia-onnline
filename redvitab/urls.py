"""redvitab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from nodos import views

urlpatterns = [
    path('', views.signin, name='signin'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('landingpage/', views.lp, name='lp'),
    #Rutas de proyectos
    path('proyectos/crear', views.proyecto, name='proyectos'),
    path('proyectos/Ver', views.proyectoListar, name='proyectoL'),
    path('proyecto/<int:id>', views.proyectoProfile, name='proyectoP'),
    path('proyecto/Borrar/<int:id>', views.proyectoDelete, name='proyectoD'),
   
    #Ruta Participantes
    path('participantes/Crear', views.participantesCreate, name='participantes'),
    path('participantes/Ver', views.participantesListar, name='participantesL'),
    path('participantes/<int:id>', views.participantesProfile, name='participantesP'),
    path('participantes/Borrar/<int:id>', views.participantesDelete, name='participantesD'),
    
    #Rutas de Instituciones
    path('miembros/Crear', views.miembrosCreate, name='miembros'),
    path('miembros/Ver', views.miembrosListar, name='miembrosL'),
    path('miembros/<int:id>', views.miembrosProfile, name='miembrosP'),
    path('miembros/Borrar/<int:id>', views.miembrosDelete, name='miembrosD'),
]
