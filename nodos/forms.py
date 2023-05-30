from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django import forms
from django.forms import ModelForm, widgets   
SEX = [
        ("1", "Masculino"),
        ("2", "Femenino"),
    ]
GRADO = [
        ("1", "LICENCIADO(A)"),
        ("2", "INGENIERO(A)"),
        ("3", "MAESTRO(A)"),
        ("4", "DOCTOR(A)"),
    ]
ESTATUS = [
        ("1", "ACTIVO(A)"),
        ("2", "INACTIVO(A)"),
        ("3", "EN PROCESO(A)"),
    ]
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model=CustomUser
        fields =('email',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class GruposForm(ModelForm):
    
    class Meta:
        model = TabGrupo
        fields= ['grup_nom', 'grup_fechac','grup_fechat' , 'grup_desc' , 'grup_integrante' , 'grup_fkenlace', 'grup_fkcoord', 'grup_fkest', 'grup_fknodo']

class proyectoform(ModelForm):
    proy_fechini = forms.DateField(widget=forms.SelectDateWidget())
    proy_fechfin = forms.DateField(widget=forms.SelectDateWidget())
    proy_coord = forms.ModelChoiceField(queryset=TabMiembro.objects.order_by('m_id').distinct(),
            empty_label=None, label=None, required=True)
    proy_sec = forms.ModelChoiceField(queryset=TabMconsejo.objects.order_by('mcon_id').distinct(),
            empty_label=None, label=None, required=True)
    class Meta:
        model = TabProyecto
        fields = '__all__'

class MiembrosForm(ModelForm):
    m_fechains = forms.DateField(widget=forms.SelectDateWidget())
    m_fkinst = forms.ModelChoiceField(queryset=TabDependencia.objects.order_by('dep_id').distinct(),
            empty_label=None, label=None, required=True)
    m_genero = forms.CharField(widget=forms.Select(choices=SEX))
    m_gradacad = forms.CharField(widget=forms.Select(choices=GRADO))
    m_estatus = forms.CharField(widget=forms.Select(choices=ESTATUS))
    m_fktipo = forms.ModelChoiceField(queryset=TabTipousuario.objects.order_by('tip_id').distinct(),
            empty_label=None, label=None, required=True)
    class Meta:
        model = TabMiembro 
        fields =['m_nomb', 'm_app','m_apm' , 'm_curp' , 'm_tel' , 'm_tel2', 'm_correo', 'm_correo2', 'm_cargo', 'm_fechains', 'm_fkinst', 'm_genero', 'm_gradacad','m_estatus', 'm_fktipo']
        widgets={
            'm_nomb':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ingrese el Nombre'}),
            'm_app':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ingrese el Apellido Paterno'}),
            'm_apm':forms.TextInput(attrs={'class':'form-control' , 'placeholder': 'Ingrese el Apellido Materno'}),
            'm_tel':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ingrese el Telefono Principal'}),
            'm_tel2':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ingrese el Telefono Secundario'}),
            'm_correo':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ingrese el Correo Principal'}),
            'm_correo2':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ingrese el Correo Secundario'}),
            'm_cargo':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ingrese el Cargo de la persona'}),
            'm_fkinst':forms.Select(attrs={'class':'form-control'}),
            'm_genero':forms.Select(attrs={'class':'form-control'}),
            'm_gradacad':forms.Select(attrs={'class':'form-control'}),
            'm_estatus':forms.Select(attrs={'class':'form-control'}),
            'm_fktipo':forms.Select(attrs={'class':'form-control'}),

           
        }


