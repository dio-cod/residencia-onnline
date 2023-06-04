from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class TabDependencia(models.Model):
    dep_id = models.AutoField(primary_key=True)
    dep_nomb = models.CharField(max_length=100)
    dep_siglas = models.CharField(max_length=10)
    dep_direccon = models.CharField(max_length=150)
    dep_localidad = models.CharField(max_length=50)
    dep_tel = models.CharField(max_length=10)
    dep_correo = models.CharField(max_length=100)
    dep_fktipo = models.ForeignKey('TabTipodependencia', models.DO_NOTHING, db_column='dep_fktipo')
    dep_fkenlace = models.ForeignKey('TabMiembro', models.DO_NOTHING, db_column='dep_fkenlace', blank=True, null=True)

    class Meta:
        db_table = 'tab_dependencia'
    def __str__(self):
        return self.dep_nomb

class TabDescgrupo(models.Model):
    dg_id = models.AutoField(primary_key=True)
    field_dg_fkgrupo = models.ForeignKey('TabGrupo', models.DO_NOTHING, db_column=' dg_fkgrupo')  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    dg_fkmiemb = models.ForeignKey('TabMiembro', models.DO_NOTHING, db_column='dg_fkmiemb')
    dg_fkestatus = models.ForeignKey('TabEstatus', models.DO_NOTHING, db_column='dg_fkestatus')

    class Meta:
        db_table = 'tab_descgrupo'    


class TabDescproyec(models.Model):
    dn_id = models.AutoField(primary_key=True)
    dn_fknodo = models.ForeignKey('TabProyecto', models.DO_NOTHING, db_column='dn_fknodo')
    dn_fkmiemb = models.ForeignKey('TabMiembro', models.DO_NOTHING, db_column='dn_fkmiemb')
    dn_fkestatus = models.ForeignKey('TabEstatus', models.DO_NOTHING, db_column='dn_fkestatus')

    class Meta:
        db_table = 'tab_descproyec'


class TabDescreunion(models.Model):
    desr_id = models.AutoField(primary_key=True)
    desr_fkmiem = models.ForeignKey('TabMiembro', models.DO_NOTHING, db_column='desr_fkmiem')
    desr_fkreu = models.ForeignKey('TabReuniong', models.DO_NOTHING, db_column='desr_fkreu')

    class Meta:
        db_table = 'tab_descreunion'

class TabEstatus(models.Model):
    est_id = models.AutoField(primary_key=True)
    est_nomb = models.CharField(max_length=15)

    class Meta:
        db_table = 'tab_estatus'
    def __str__(self):
            return self.est_nomb

class TabMiembro(models.Model):
    m_id = models.AutoField(primary_key=True)
    m_nomb = models.CharField(max_length=50)
    m_app = models.CharField(max_length=50)
    m_apm = models.CharField(max_length=30)
    m_curp = models.CharField(max_length=18, blank=True, null=True)
    m_tel = models.CharField(max_length=10)
    m_tel2 = models.CharField(max_length=10, blank=True, null=True)
    m_correo = models.CharField(max_length=80)
    m_correo2 = models.CharField(max_length=80, blank=True, null=True)
    m_cargo = models.CharField(max_length=100)
    m_fechains = models.DateField()
    m_fkinst = models.ForeignKey(TabDependencia, models.DO_NOTHING, db_column='m_fkinst')
    m_genero = models.IntegerField()
    m_gradacad = models.IntegerField()
    m_estatus = models.IntegerField()
    m_fktipo = models.ForeignKey('TabTipousuario', models.DO_NOTHING, db_column='m_fktipo')
    m_fkuser = models.ForeignKey(CustomUser, models.DO_NOTHING, db_column='m_fkuser', null=True)
    
    class Meta:
        db_table = 'tab_miembro' 
    def __str__(self):
            return self.m_nomb+' '+self.m_app+' '+ self.m_apm

class TabGrupo(models.Model):
    grup_id = models.AutoField(primary_key=True)
    grup_nom = models.CharField(max_length=150)
    grup_fechac = models.DateField()
    grup_fechat = models.DateField()
    grup_desc = models.TextField(blank=True, null=True)
    grup_integrante = models.IntegerField()
    grup_fkenlace = models.ForeignKey('TabMconsejo', models.DO_NOTHING, db_column='grup_fkenlace')
    grup_fkcoord = models.ForeignKey('TabMiembro', models.DO_NOTHING, db_column='grup_fkcoord')
    grup_fkest = models.ForeignKey(TabEstatus, models.DO_NOTHING, db_column='grup_fkest')
    grup_fknodo = models.ForeignKey('TabProyecto', models.DO_NOTHING, db_column='grup_fknodo')

    class Meta:
        db_table = 'tab_grupo'
    def __str__(self):
            return self.grup_nom     

class TabMconsejo(models.Model):
    mcon_id = models.AutoField(primary_key=True)
    mcon_nomb = models.CharField(max_length=50)
    mcon_app = models.CharField(max_length=30)
    mcon_apm = models.CharField(max_length=30)
    mcon_tel = models.CharField(max_length=10)
    mcon_correo = models.CharField(max_length=60)
    mcon_correo2 = models.CharField(max_length=60, blank=True, null=True)
    mcon_fktipou = models.ForeignKey('TabTipousuario', models.DO_NOTHING, db_column='mcon_fktipou')

    class Meta:
        db_table = 'tab_mconsejo'
    def __str__(self):
            return self.mcon_nomb+' '+ self.mcon_app +' '+self.mcon_apm
 

class TabProyecto(models.Model):
    proy_id = models.AutoField(primary_key=True)
    proy_nomb = models.CharField(max_length=25)
    proy_tipo = models.CharField(max_length=15)
    proy_desc = models.CharField(max_length=150, blank=True, null=True)
    proy_fechini = models.DateField()
    proy_fechfin = models.DateField()
    proy_coord = models.ForeignKey(TabMiembro, models.DO_NOTHING, db_column='proy_coord')
    proy_sec = models.ForeignKey(TabMconsejo, models.DO_NOTHING, db_column='proy_sec')
    class Meta:
        db_table = 'tab_proyecto'
    def __str__(self):
            return self.proy_nomb 


class TabReuniong(models.Model):
    reu_id = models.AutoField(primary_key=True)
    reu_nomb = models.CharField(max_length=255, blank=True, null=True)
    reu_participante = models.IntegerField()
    reu_obs = models.TextField()
    reu_plat = models.CharField(max_length=100)
    reu_fecha = models.DateField()
    reu_fkgrup = models.ForeignKey(TabGrupo, models.DO_NOTHING, db_column='reu_fkgrup', blank=True, null=True)
    reu_fkproyect = models.ForeignKey(TabProyecto, models.DO_NOTHING, db_column='reu_fkproyect')
    reu_fktipo = models.ForeignKey('TabTiporeunion', models.DO_NOTHING, db_column='reu_fktipo')

    class Meta:
        db_table = 'tab_reuniong'
    def __str__(self):
            return self.reu_nomb 

class TabTiporeunion(models.Model):
    tipreu_id = models.AutoField(primary_key=True)
    tipreu_nomb = models.CharField(max_length=45)

    class Meta:
        db_table = 'tab_tiporeunion'
    def __str__(self):
            return self.tipreu_nomb         

class TabTipodependencia(models.Model):
    tipodep_id = models.AutoField(primary_key=True)
    tipodep_nomb = models.CharField(max_length=50)

    class Meta:
        db_table = 'tab_tipodependencia'
    def __str__(self):
            return self.tipodep_nomb 

class TabTipousuario(models.Model):
    tip_id = models.AutoField(primary_key=True)
    tip_nomb = models.CharField(max_length=30)

    class Meta:
        db_table = 'tab_tipousuario'
    def __str__(self):
            return self.tip_nomb 