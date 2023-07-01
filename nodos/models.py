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


class TabAcuerdoreunion(models.Model):
    acu_id = models.IntegerField(primary_key=True)
    acu_cod = models.CharField(max_length=15)
    acu_fktipo = models.ForeignKey('TabTipoacuerdo', models.DO_NOTHING, db_column='acu_fktipo')
    acu_fcompromiso = models.DateField()
    acu_fkestatus = models.ForeignKey('TabEstatus', models.DO_NOTHING, db_column='acu_fkestatus')
    acu_fkreunion = models.ForeignKey('TabReunion', models.DO_NOTHING, db_column='acu_fkreunion')

    class Meta:
        managed = True
        db_table = 'tab_acuerdoreunion'


class TabDescgrupo(models.Model):
    dg_id = models.AutoField(primary_key=True)
    dg_fkgrupo = models.ForeignKey('TabGrupo', models.DO_NOTHING, db_column='dg_fkgrupo')
    dg_fkmiemb = models.ForeignKey('TabMiembro', models.DO_NOTHING, db_column='dg_fkmiemb')
 
    class Meta:
        managed = True
        db_table = 'tab_descgrupo'

class TabDescreunion(models.Model):
    desr_id = models.AutoField(primary_key=True)
    desr_fkmiem = models.ForeignKey('TabMiembro', models.DO_NOTHING, db_column='desr_fkmiem')
    desr_fkreu = models.ForeignKey('TabReunion', models.DO_NOTHING, db_column='desr_fkreu')

    class Meta:
        managed = True
        db_table = 'tab_descreunion'


class TabEstatus(models.Model):
    est_id = models.AutoField(primary_key=True)
    est_nomb = models.CharField(max_length=15)

    class Meta:
        managed = True
        db_table = 'tab_estatus'
    def __str__(self):
        return self.est_nomb 


class TabGrupo(models.Model):
    grup_id = models.AutoField(primary_key=True)
    grup_nom = models.CharField(max_length=150)
    grup_fechac = models.DateField()
    grup_fechat = models.DateField()
    grup_desc = models.TextField(blank=True, null=True)
    grup_integrante = models.IntegerField()
    grup_fkenlace = models.ForeignKey('TabMiembro', on_delete=models.SET_NULL, db_column='grup_fkenlace',null=True)
    grup_fkcoord = models.ForeignKey('TabMconsejo', on_delete=models.SET_NULL, db_column='grup_fkcoord',null=True)
    grup_fkest = models.ForeignKey(TabEstatus, on_delete=models.SET_NULL, db_column='grup_fkest',null=True)
    grup_fkproyecto = models.ForeignKey('TabProyecto', on_delete=models.SET_NULL, db_column='grup_fkproyecto',null=True)

    class Meta:
        managed = True
        db_table = 'tab_grupo'


class TabInstitucion(models.Model):
    ins_id = models.AutoField(primary_key=True)
    ins_nomb = models.CharField(max_length=255)
    ins_sigla = models.CharField(max_length=20, blank=True, null=True)
    ins_dir = models.CharField(max_length=150)
    ins_localidad = models.CharField(max_length=50)
    ins_tel = models.CharField(max_length=10)
    ins_correo = models.CharField(max_length=100)
    ins_fktipo = models.ForeignKey('TabTipodependencia', models.DO_NOTHING, db_column='ins_fktipo', null=True)
    ins_fkenlace = models.ForeignKey('TabMiembro', models.DO_NOTHING, db_column='ins_fkenlace', blank=True, null=True)
    ins_subcat = models.CharField(max_length=155)

    class Meta:
        managed = True
        db_table = 'tab_institucion'
    def __str__(self):
        return self.ins_nomb


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
        managed = True
        db_table = 'tab_mconsejo'
    def __str__(self):
        return self.mcon_nomb +" "+self.mcon_app+" "+self.mcon_apm

class TabMiembro(models.Model):
    m_id = models.AutoField(primary_key=True)
    m_curp = models.CharField(max_length=13, blank=True, null=True)
    m_nomb = models.CharField(max_length=50)
    m_app = models.CharField(max_length=50)
    m_apm = models.CharField(max_length=30)
    m_tel = models.CharField(max_length=10)
    m_tel2 = models.CharField(max_length=10, blank=True, null=True)
    m_correo = models.CharField(max_length=80)
    m_correo2 = models.CharField(max_length=80, blank=True, null=True)
    m_cargo = models.CharField(max_length=100)
    m_fechains = models.DateField()
    m_fkinst = models.ForeignKey(TabInstitucion,on_delete=models.SET_NULL, db_column='m_fkinst' ,null=True)
    m_genero = models.IntegerField()
    m_gradacad = models.IntegerField()
    m_estatus = models.IntegerField()
    m_fktipo = models.ForeignKey('TabTipousuario', models.DO_NOTHING, db_column='m_fktipo')  
    m_fkuser = models.ForeignKey(CustomUser, models.DO_NOTHING, db_column='m_fkuser', null=True)
    class Meta:
        managed = True
        db_table = 'tab_miembro'
    def __str__(self):
        return self.m_apm+ " "+self.m_app+ " "+ self.m_nomb

class TabProyecto(models.Model):
    proy_id = models.AutoField(primary_key=True)
    proy_nomb = models.CharField(max_length=255)
    proy_tipo = models.CharField(max_length=15)
    proy_desc = models.TextField()
    proy_fechini = models.DateField()
    proy_fechfin = models.DateField()
    proy_estatus = models.ForeignKey('TabEstatus', models.DO_NOTHING, db_column='dp_fkestatus')
    proy_coord = models.ForeignKey(TabMconsejo, models.DO_NOTHING, db_column='proy_coord')
    proy_miemb = models.ManyToManyField(TabMiembro, through="TabProyectoProyMiemb")
    class Meta:
        managed = True
        db_table = 'tab_proyecto'
    def __str__(self):
        return self.proy_nomb

class TabProyectoProyMiemb(models.Model):
    id = models.BigAutoField(primary_key=True)
    tabproyecto = models.ForeignKey(TabProyecto, models.DO_NOTHING)
    tabmiembro = models.ForeignKey(TabMiembro, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tab_proyecto_proy_miemb'
        unique_together = (('tabproyecto', 'tabmiembro'),)

class TabReunion(models.Model):
    reu_id = models.AutoField(primary_key=True)
    reu_cod = models.CharField(max_length=10, db_comment='CODIGO DE LA REUNION')
    reu_nomb = models.CharField(max_length=255, blank=True, null=True, db_comment='NOMBRE DE LA REUNION')
    reu_participante = models.IntegerField(db_comment='CANTIDAD DE PARTICIPANTES EN LA REUNIËN')
    reu_obs = models.TextField(db_comment='DESCRIPCION DE LA REUNION')
    reu_medio = models.CharField(max_length=100)
    reu_fecha = models.DateField()
    reu_fkgrup = models.ForeignKey(TabGrupo, models.DO_NOTHING, db_column='reu_fkgrup')
    reu_fkproyect = models.ForeignKey(TabProyecto, models.DO_NOTHING, db_column='reu_fkproyect')
    reu_fktipo = models.ForeignKey('TabTiporeunion', models.DO_NOTHING, db_column='reu_fktipo')
    reu_fkcoor = models.ForeignKey(TabMconsejo, models.DO_NOTHING, db_column='reu_fkcoor')

    class Meta:
        managed = True
        db_table = 'tab_reunion'


class TabTipoacuerdo(models.Model):
    tipa_id = models.IntegerField(primary_key=True)
    tipa_nomb = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'tab_tipoacuerdo'


class TabTipodependencia(models.Model):
    tipodep_id = models.AutoField(primary_key=True)
    tipodep_nomb = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'tab_tipodependencia'
    
    def __str__(self):
        return self.tipodep_nomb

class TabTiporeunion(models.Model):
    tipreu_id = models.AutoField(primary_key=True)
    tipreu_nomb = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'tab_tiporeunion'


class TabTipousuario(models.Model):
    tip_id = models.AutoField(primary_key=True)
    tip_nomb = models.CharField(max_length=30)

    class Meta:
        managed = True
        db_table = 'tab_tipousuario'
    def __str__(self):
        return self.tip_nomb