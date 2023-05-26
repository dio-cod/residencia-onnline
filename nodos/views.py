from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import *
from .decorators import allowed_users
# Create your views here.


def home(request):
    return render(request, 'home.html', {
        'form': UserCreationForm
    })


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
                    'error': 'Username already exists'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Passwords do not match'
        })

@login_required
def signout(request):
    logout(request)
    return redirect('home')


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
            'error':'Username or password is incorrect'
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
@allowed_users(allowed_roles=['Miembro'])        
def miembrosListar(request):
    listaMiembros=TabMiembro.objects.all()
    return render(request, 'miembroslista.html',{
        'miembros':listaMiembros
    })


@login_required
@allowed_users(allowed_roles=['Enlaces'])
def miembrosCreate(request):
    if request.method=='GET':
        return render(request, 'miembro.html',{
            'form': MiembrosForm
        })
    else:
         form=MiembrosForm(request.POST)
         print(request.POST)
         if form.is_valid():
            new_miembro=form.save(commit=False)
            new_miembro.save()
            return redirect ('lp')
         else:
             return render(request, 'miembro.html', {
            'form': MiembrosForm,
            'error':'Favor de rellenar todos los campos'
             })