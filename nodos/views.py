from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import *
from .decorators import allowed_users
# Create your views here.


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': CustomUserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            print(request.POST)
            try:
                user = CustomUser.objects.create_user(
                    email=request.POST['email'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('lp')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Ya existe un correo asociado'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
        })

@login_required
def signout(request):
    logout(request)
    return redirect('signin')


@login_required
def lp(request):
    return render(request, 'lp.html')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm 
        })
    else:
        user=authenticate(
            request, username=request.POST['username'], password=request.POST['password']) #Aqui se llama username porque se usa el formulario de django pero es el correo
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error':'El correo o la contraseña son incorrectos'
             })
        else:
            login(request, user)     
        return redirect('lp')
    
@login_required
@allowed_users(allowed_roles=['Enlaces']) 
def proyecto(request):
    if request.method=='GET':
        return render(request, 'grupo.html',{
            'form': proyectoform
        })
    else:
         form=proyectoform(request.POST)
         if form.is_valid():
            new_director=form.save(commit=False)
            new_director.save()
            return redirect ('lp')
         else:
             return render(request, 'grupo.html', {
            'form': proyectoform,
            'error':'Favor de rellenar todos los campos'
             })


@login_required
@allowed_users(allowed_roles=['Miembro', 'Enlaces'])        
def participantesListar(request):
    listaParticipante=TabMiembro.objects.all()
    return render(request, 'participantesslista.html',{
        'miembros':listaParticipante
    })


@login_required
@allowed_users(allowed_roles=['Enlaces'])
def participantesCreate(request):

    if request.method=='GET':
        return render(request, 'nuevoParticipante.html',{
            'form': ParticipanteForm
        })
    else:
         form=ParticipanteForm(request.POST)
         print(request.POST)
         if form.is_valid():
            new_miembro=form.save(commit=False)
            new_miembro.save()
            return redirect ('lp')
         else:
             return render(request, 'participante.html', {
            'form': ParticipanteForm,
            'error':'Favor de rellenar todos los campos'
             })

@login_required
@allowed_users(allowed_roles=['Enlaces'])
def participantesProfile(request, id):
  if request.method=='GET':
    participante=get_object_or_404(TabMiembro, m_id=id)
    form= ParticipanteForm(instance=participante) 
    return render (request, 'participantesprof.html', {
        'participante':participante,
        'form':form
    })
  else:
      participante=get_object_or_404(TabMiembro, m_id=id)
      form=ParticipanteForm(request.POST, instance=participante)
      form.save()
      return redirect('participantesL')

@login_required
@allowed_users(allowed_roles=['Miembro', 'Enlaces'])        
def proyectoListar(request):
    listaProyectos=TabProyecto.objects.all()
    print(listaProyectos)
    return render(request, 'proyectoslista.html',{
        'proyectos':listaProyectos
    })

@login_required
@allowed_users(allowed_roles=['Enlaces'])
def proyectoProfile(request, id):
  if request.method=='GET':
    proyecto=get_object_or_404(TabProyecto, proy_id=id)
    form= proyectoform(instance=proyecto) 
    return render (request, 'proyectoprof.html', {
        'proyecto':proyecto,
        'form':form
    })
  else:
      proyecto=get_object_or_404(TabProyecto, proy_id=id)
      form=proyectoform(request.POST, instance=proyecto)
      form.save()
      return redirect('proyectoL')
