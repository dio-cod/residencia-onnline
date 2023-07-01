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


#Inicio y Cierre de Sesión
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

#Registro de usuario
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
def participantesListar(request):
    listaParticipante=TabMiembro.objects.all() #traigo todos los objetos para mostrarlos en la vista
    return render(request, 'participantesslista.html',{
        'miembros':listaParticipante    #Los envio a la plantilla para poder accesar a ellos
    })

@login_required
def participantesCreate(request):
    if request.method=='GET': #Valido la petición
        return render(request, 'nuevoParticipante.html',{
            'form': ParticipanteForm    #le mando el formulario que cree en forms.py 
        })
    else:
         form=ParticipanteForm(request.POST)#Almaceno la respuesta en un form 
         print(request.POST)#recibo e imprimo los datos en consola para que corrobore que se enviaron correctamente
         if form.is_valid():#hago una validación simple de que cumplan con los requisitos de los campos según las validaciones de la DB
            new_participante=form.save(commit=False)#almaceno el form en una variable y le doy commit false para que no intente guardarlo y me devuelva los datos
            new_participante.save()#ya este es un objeto y uso save para guardar los datos en la db
            return redirect ('participantesL')#redirecciono a esa ruta, los nombres de las rutas estan en url.py
         else:
             return render(request, 'participante.html', { #si me marca un error le devuelvo el formulario y un error, ojo aca yo puse ese por defecto no dice cual es el error exacto
            'form': ParticipanteForm,
            'error':'Favor de rellenar todos los campos'
             })

@login_required
def participantesProfile(request, id):#ACA PIDO UN ID QUE ME ENVIA DESDE LA URL, CHECA EN EL HTML EL BOTON VER 
  if request.method=='GET':#ACA VUELVO A VALIDAR LA PETICIÓN
    participante=get_object_or_404(TabMiembro, m_id=id)# USO ESTA FUNCION PQ SOLO QUIERO UN OBJETO SI ES QUE LO ENCUENTRA 
    par= participante.tabproyecto_set.all()
    
    form = ParticipanteForm(instance=participante) #ALMACENO LOS DATOS EN EL FORM PARA MOSTRARLOS 
    return render (request, 'participantesprof.html', {
        'participante':participante,
        'form':form,
        'par':par
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

@login_required
def participantesDelete(request, id):
    pt= get_object_or_404(TabMiembro, m_id=id)
    try:
        pt.delete()
    except:
        print("no se pudo borrar")
    return participantesListar(request)

#Proyecto    
@login_required
def proyecto(request):
    if request.method=='GET':
        return render(request, 'proyecto.html',{
            'form': proyectoform
        })
    else:
         form=proyectoform(request.POST) #guardo el POST en form para poder validarlo
         if form.is_valid():    #valido
            pr=form.save(commit=False) #creo el objeto pr
            miemb = request.POST.getlist('proy_miemb')#obtengo los id de los miembros que participan 
            pr.save() #guardo el objeto pr
            for x in miemb: #aquí hago un for para que recorra el arreglo de id de los miembros y por cada dato que lea los vaya guardando en la tabla proyecto
             pr.proy_miemb.add(x)
            return redirect ('proyectoL')
         else:
             return render(request, 'proyecto.html', {
            'form': proyectoform,
            'error':'Favor de rellenar todos los campos'
             })

@login_required    
def proyectoListar(request):
    listaProyectos=TabProyecto.objects.all()
    return render(request, 'proyectoslista.html',{
        'proyectos':listaProyectos
    })

@login_required
def proyectoProfile(request, id):
  if request.method=='GET':
    proyecto=get_object_or_404(TabProyecto, proy_id=id)
    p1=proyecto.proy_miemb.all()
    form=proyectoform(instance=proyecto)
    part=TabProyectoProyMiemb.objects.filter(tabproyecto_id=id)
   
    return render (request, 'proyectoprof.html', {
        'form':form,
        'part':p1
    })
  else:
    try:
      proyecto=get_object_or_404(TabProyecto, proy_id=id)
      form=proyectoform(request.POST, instance=proyecto)
      if form.is_valid():
        form.save()
      else:
          print("no se pudo ")  
      return redirect('proyectoL')
    except ValueError:# Si no funciona por x le mando este error predeterminado
           return render (request, 'participantesprof.html', {
        'form':form,
        'error':'Error Actualizando'
    })

@login_required     
def proyectoDelete(request, id):
    try:
        proyecto = get_object_or_404(TabProyecto, proy_id=id)
        proyecto.delete()
        msg="SE HA BORRADO SATISFACTORIAMENTE"
        lista=TabProyecto.objects.all()
        return render(request, 'proyectoslista.html',{
             'msg':msg,
             'proyectos':lista
        })
    except:
        return  render(request, 'proyectoslista.html', {
            'msg':"Ha habido un error al borrar"
        })

#Miembros de la red O Instituciones
@login_required
def miembrosListar(request):
    miembros=TabInstitucion.objects.all()
    return render(request,'miembroslista.html',{
        'miembros':miembros
    })

@login_required
def miembrosCreate(request):
    if request.method=="GET":
        return render(request, "miembro.html", {
            'form':miembroform
        })     
    else:
        form = miembroform (request.POST)
        if form.is_valid():
            new_miembro= form.save(commit=False)
            new_miembro.save()
            return redirect("miembrosL")

@login_required
def miembrosProfile(request, id):
    if request.method=='GET':
     inst=get_object_or_404(TabInstitucion, ins_id=id)
     form=miembroform(instance=inst)
     return render (request, 'miembroProf.html', {
        'form':form
    })
    else:
      try:
          inst=get_object_or_404(TabInstitucion, ins_id=id)#OBTENGO LOS DATOS DE NUEVO
          form=miembroform(request.POST, instance=inst)#ALMACENO LOS DATOS DEL POST EN EL FORM Y LA INSTANCIA DE LA TAREA YA CREADA PARA EDITARLA
          form.save()#GUARDO Y REDIRECCIONO 
          return redirect('miembrosL')
      except ValueError:# Si no funciona por x le mando este error predeterminado
           return render (request, 'participantesprof.html', {
        'participante':inst,
        'form':form,
        'error':'Error Actualizando'
    })

@login_required     
def miembrosDelete(request, id):
     inst = get_object_or_404(TabInstitucion, ins_id=id)
     try:
       inst.delete()
     except:
        print("no se pudo borrar")
     return miembrosListar(request)


