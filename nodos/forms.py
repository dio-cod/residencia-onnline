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
SUBCAT=[
    ('1', "SUBCATEGORIA 1"),
    ('2', "SUBCATEGORIA 2"),
    ('3', "SUBCATEGORIA 3")
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
        fields= ['grup_nom', 'grup_fechac','grup_fechat' , 'grup_desc' , 'grup_integrante' , 'grup_fkenlace', 'grup_fkcoord', 'grup_fkest']

class proyectoform(ModelForm):
    proy_coord = forms.ModelChoiceField(queryset=TabMiembro.objects.distinct(),required=True).widget_attrs
    proy_sec = forms.ModelChoiceField(queryset=TabMconsejo.objects.distinct(),required=True).widget_attrs
    class Meta:
        model = TabProyecto
        fields = '__all__'
        widgets={
            'proy_nomb':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ingrese el Nombre del Proyecto'}),
            'proy_tipo':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ingrese el tipo de proyecto'}),
            'proy_desc':forms.TextInput(attrs={'class':'form-control' , 'placeholder': 'Ingrese la descripción del proyecto'}),
            'proy_fechini':forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'proy_fechfin':forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'proy_estatus':forms.Select(attrs={'class':'form-control'}),
            'proy_coord':forms.Select(attrs={'class':'form-control'}),
            'proy_miemb':forms.SelectMultiple(attrs={'class':'form-control'})
        }

class ParticipanteForm(ModelForm):
    m_fechains = forms.DateField(widget=forms.SelectDateWidget()).widget_attrs
    m_fkinst = forms.ModelChoiceField(queryset=TabInstitucion.objects.distinct(), required=True).widget_attrs
    m_fktipo = forms.ModelChoiceField(queryset=TabTipousuario.objects.distinct(), required=True).widget_attrs
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
            'm_fechains':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'm_fkinst':forms.Select(attrs={'class':'form-control'},),
            'm_genero':forms.Select(attrs={'class':'form-control'}, choices=SEX),
            'm_gradacad':forms.Select(attrs={'class':'form-control'}, choices=GRADO),
            'm_estatus':forms.Select(attrs={'class':'form-control'}, choices=ESTATUS),
            'm_fktipo':forms.Select(attrs={'class':'form-control'}),
        }

class miembroform(ModelForm):
   class Meta:
        model = TabInstitucion
        fields = '__all__'
        widgets={
            'ins_nomb':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ingrese el Nombre'}),
            'ins_sigla':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ingrese el Apellido Paterno'}),
            'ins_dir':forms.TextInput(attrs={'class':'form-control' , 'placeholder': 'Ingrese el Apellido Materno'}),
            'ins_localidad':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ingrese el Telefono Principal'}),
            'ins_tel':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ingrese el Telefono Secundario'}),
            'ins_correo':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Ingrese el Correo Principal'}),
            'ins_fktipo':forms.Select(attrs={'class':'form-control'}),
            'ins_fkenlace':forms.Select(attrs={'class':'form-control'}),
            'ins_subcat':forms.Select(attrs={'class':'form-control', 'placeholder': 'Ingrese el Cargo de la persona'},  choices=SUBCAT),
        }

