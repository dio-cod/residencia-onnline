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

#Participantes
@login_required
@allowed_users(allowed_roles=['Miembro', 'Enlaces'])        
def participantesListar(request):
    listaParticipante=TabMiembro.objects.all() #traigo todos los objetos para mostrarlos en la vista
    return render(request, 'participantesslista.html',{
        'miembros':listaParticipante    #Los envio a la plantilla para poder accesar a ellos
    })

@login_required
@allowed_users(allowed_roles=['Enlaces'])
def participantesCreate(request):
    if request.method=='GET': #Valido la petición
        return render(request, 'nuevoParticipante.html',{
            'form': ParticipanteForm    #le mando el formulario que cree en forms.py 
        })
    else:
         form=ParticipanteForm(request.POST)#Almaceno la respuesta en un form 
         print(request.POST)#recibo e imprimo los datos en consola para que corrobore que se enviaron correctamente
         if form.is_valid():#hago una validación simple de que cumplan con los requisitos de los campos según las validaciones de la DB
            new_miembro=form.save(commit=False)#almaceno el form en una variable y le doy commit false para que no intente guardarlo y me devuelva los datos
            new_miembro.save()#ya este es un objeto y uso save para guardar los datos en la db
            return redirect ('participantesL')#redirecciono a esa ruta, los nombres de las rutas estan en url.py
         else:
             return render(request, 'participante.html', { #si me marca un error le devuelvo el formulario y un error, ojo aca yo puse ese por defecto no dice cual es el error exacto
            'form': ParticipanteForm,
            'error':'Favor de rellenar todos los campos'
             })

@login_required
@allowed_users(allowed_roles=['Enlaces'])
def participantesProfile(request, id):#ACA PIDO UN ID QUE ME ENVIA DESDE LA URL, CHECA EN EL HTML EL BOTON VER 
  if request.method=='GET':#ACA VUELVO A VALIDAR LA PETICIÓN
    participante=get_object_or_404(TabMiembro, m_id=id)# USO ESTA FUNCION PQ SOLO QUIERO UN OBJETO SI ES QUE LO ENCUENTRA 
    form = ParticipanteForm(instance=participante) #ALMACENO LOS DATOS EN EL FORM PARA MOSTRARLOS 
    return render (request, 'participantesprof.html', {
        'participante':participante,
        'form':form
    })
  else:
      try:
          participante=get_object_or_404(TabMiembro, m_id=id)#OBTENGO LOS DATOS DE NUEVO
          form=ParticipanteForm(request.POST, instance=participante)#ALMACENO LOS DATOS DEL POST EN EL FORM Y LA INSTANCIA DE LA TAREA YA CREADA PARA EDITARLA
          form.save()#GUARDO Y REDIRECCIONO 
          return redirect('participantesL')
      except ValueError:# Si no funciona por x le mando este error predeterminado
           return render (request, 'participantesprof.html', {
        'participante':participante,
        'form':form,
        'error':'Error Actualizando'
    })
#Proyecto
    
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
def proyectoListar(request):
    listaProyectos=TabProyecto.objects.all()
    return render(request, 'proyectoslista.html',{
        'proyectos':listaProyectos
    })

@login_required
@allowed_users(allowed_roles=['Enlaces'])
def proyectoProfile(request, id):
  if request.method=='GET':
    proyecto=get_object_or_404(TabProyecto, proy_id=id)
    details= TabDescproyec.objects.filter(dn_fknodo=id)
    form=proyectoform(instance=proyecto) 
    
    return render (request, 'proyectoprof.html', {
        'form':form,
        'form2':desc_proyectoform,
        'details':details
    })
  else:
      proyecto=get_object_or_404(TabProyecto, proy_id=id)
      form=proyectoform(request.POST, instance=proyecto)
      form.save()
      return redirect('proyectoL')


#Miembros de la red
@login_required
def miembrosListar(request):
    miembros=TabDependencia.objects.all()
    return render(request,'miembroslista.html',{
        'miembros':miembros
    })


@login_required
def miembrosCreate(request):
    return 
