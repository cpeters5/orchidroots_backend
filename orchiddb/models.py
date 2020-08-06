from django.db import models
# from django.contrib.auth.models import (
#     BaseUserManager, AbstractBaseUser
# )
import six
from mptt.models import MPTTModel, TreeForeignKey
from django.dispatch import receiver
from PIL import Image as Img
from PIL import ExifTags
from io import BytesIO
import os, shutil
from django.core.files import File
from django.db.models.signals import post_save
from django.conf import settings
from django.utils import timezone

from utils.utils import rotate_image
from accounts.models import User, Photographer
import re
import math
RANK_CHOICES = [(i,str(i)) for i in range(0,10)]
QUALITY = (
    (1, 'Top'),
    (2, 'High'),
    (3, 'Average'),
    (4, 'Low'),
    # (5, 'Challenged'),
)

STATUS_CHOICES = [('accepted','accepted'),('registered','registered'),('nonregistered','nonregistered'),('unplaced','unplaced'),('published','published'),('trade','trade')]
TYPE_CHOICES = [('species','species'),('hybrid','hybrid')]
class Publisher(models.Model):
    author_id = models.CharField(max_length=50, primary_key=True)
    fullname = models.CharField(max_length=50)
    affiliation = models.CharField(max_length=200, blank=True)
    url = models.CharField(max_length=200, blank=True)
    web = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=10, default='TBD')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    expertise = models.CharField(max_length=500, null=True)

    @property
    def __str__(self):
        return self.fullname

# Genera


class Family(models.Model):
    family = models.CharField(primary_key=True, default='', db_column='family', max_length=50)
    author = models.CharField(max_length=200, blank=True)
    year = models.IntegerField(null=True)
    description = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.family
    class Meta:
        ordering = ['family']


class Subfamily(models.Model):
    family = models.ForeignKey(Family, default='', db_column='family',on_delete=models.DO_NOTHING)
    subfamily = models.CharField(primary_key=True,max_length=50,default='', db_column='subfamily')
    author = models.CharField(max_length=200, blank=True)
    year = models.IntegerField(null=True)
    description = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subfamily
    class Meta:
        ordering = ['subfamily']


class Tribe(models.Model):
    tribe = models.CharField(primary_key=True, default='', db_column='tribe',max_length=50)
    author = models.CharField(max_length=200, blank=True)
    year = models.IntegerField(null=True)
    subfamily = models.ForeignKey(Subfamily, null=True, default='', db_column='subfamily',on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tribe
    class Meta:
        ordering = ['tribe']


class Subtribe(models.Model):
    subtribe = models.CharField(max_length=50,primary_key=True, default='', db_column='subtribe')
    author = models.CharField(max_length=200, blank=True)
    year = models.IntegerField(null=True)
    subfamily = models.ForeignKey(Subfamily, null=True, default='', db_column='subfamily',on_delete=models.DO_NOTHING)
    tribe  = models.ForeignKey(Tribe, null=True, default='', db_column='tribe',on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subtribe
    class Meta:
        ordering = ['subtribe']


class Genus(models.Model):
    pid = models.IntegerField(primary_key=True)
    is_hybrid = models.CharField(max_length=1, null=True)
    genus = models.CharField(max_length=50, default='')
    author = models.CharField(max_length=200, default='')
    citation = models.CharField(max_length=200, default='')
    cit_status = models.CharField(max_length=20, null=True)
    alliance = models.CharField(max_length=50, default='')
    family = models.ForeignKey(Family, null=True, default='', db_column='family',on_delete=models.DO_NOTHING)
    subfamily = models.ForeignKey(Subfamily, null=True, default='', db_column='subfamily',on_delete=models.DO_NOTHING)
    tribe  = models.ForeignKey(Tribe, null=True, default='', db_column='tribe',on_delete=models.DO_NOTHING)
    subtribe  = models.ForeignKey(Subtribe, null=True, default='', db_column='subtribe',on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20, default='')
    type = models.CharField(max_length=20, default='')
    description = models.TextField(null=True)
    distribution = models.TextField(null=True)
    text_data = models.TextField(null=True)
    source = models.CharField(max_length=50, default='')
    abrev = models.CharField(max_length=50, default='')
    year = models.IntegerField(null=True)
    num_species = models.IntegerField(null=True,default=0)
    num_species_synonym = models.IntegerField(null=True,default=0)
    num_species_total = models.IntegerField(null=True,default=0)
    num_hybrid  = models.IntegerField(null=True,default=0)
    num_hybrid_synonym  = models.IntegerField(null=True, default=0)
    num_hybrid_total  = models.IntegerField(null=True,default=0)
    num_synonym  = models.IntegerField(null=True,default=0)
    num_spcimage = models.IntegerField(null=True,default=0)
    num_spc_with_image = models.IntegerField(null=True,default=0)
    pct_spc_with_image = models.DecimalField(decimal_places=2, max_digits=7,null=True,default=0)
    num_hybimage = models.IntegerField(null=True,default=0)
    num_hyb_with_image = models.IntegerField(null=True,default=0)
    pct_hyb_with_image = models.DecimalField(decimal_places=2, max_digits=7,null=True,default=0)
    notepad = models.CharField(max_length=500, default='')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.genus

    def fullname(self):
        fname = self.genus
        if self.author:
            fname = fname + self.author
        if self.year:
            fname = fname + ' ' + self.year
        return fname

    def get_status(self):
        return self.status

    def get_description(self):
        return self.description

    def getAccepted(self):
        if 'synonym' in self.status:
            acc_id = Gensyn.objects.get(pid=self.pid).acc_id
            gen = Genus.objects.get(pid=acc_id)
            return "%s <i>%s</i>" % (gen.genus, gen.author)

    def getAcc(self):
        if 'synonym' in self.status:
            acc_id = Gensyn.objects.get(pid=self.pid).acc_id
            if acc_id:
                gen = Genus.objects.get(pid=acc_id)
                return gen.genus
            else:
                return "No accepted name found for this synonym."


    def getGenid(self):
        if 'synonym' in self.status:
            syn = Gensyn.objects.get(pid=self.pid).acc_id
            return "%s" % syn

    def getSynAuth(self):
        if 'synonym' in self.status:
            syn = Gensyn.objects.get(pid=self.pid).acc_author
            return "%s" % syn

    def get_roundspcpct(self):
        if self.pct_spc_with_image > 0:
            return round(self.pct_spc_with_image)
        else: return None

    def get_roundhybpct(self):
        if self.pct_hyb_with_image > 0:
            return round(self.pct_hyb_with_image)
        else: return None


    class Meta:
        # verbose_name_plural = "Anni"
        ordering = ('genus',)


class GenusRelation(models.Model):
    gen = models.OneToOneField(Genus, db_column='gen',primary_key=True,on_delete=models.DO_NOTHING)
    genus = models.CharField(max_length=50, default='')
    parentlist = models.CharField(max_length=500, null=True)
    formula = models.CharField(max_length=500, null=True)

    def get_parentlist(self):
        x = self.parentlist.split('|')
        return x


class Genusacc(models.Model):
    # pid = models.IntegerField(primary_key=True)
    pid = models.OneToOneField(
        Genus,
        db_column='pid',
        on_delete=models.CASCADE,
        primary_key=True)
    # pid = models.ForeignKey(Genus, verbose_name='genus', db_column='pid',related_name='gen_gen', primary_key=True,on_delete=models.DO_NOTHING)
    is_hybrid = models.CharField(max_length=1, null=True)
    genus = models.CharField(max_length=50, default='')
    author = models.CharField(max_length=200, default='')
    citation = models.CharField(max_length=200, default='')
    alliance = models.CharField(max_length=50, default='')
    family = models.ForeignKey(Family, null=True, default='', db_column='family',on_delete=models.DO_NOTHING)
    subfamily = models.ForeignKey(Subfamily, null=True, default='', db_column='subfamily',on_delete=models.DO_NOTHING)
    tribe  = models.ForeignKey(Tribe, null=True, default='', db_column='tribe',on_delete=models.DO_NOTHING)
    subtribe  = models.ForeignKey(Subtribe, null=True, default='', db_column='subtribe',on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20, default='')
    type = models.CharField(max_length=20, default='')
    description = models.TextField(null=True)
    distribution = models.TextField(null=True)
    text_data = models.TextField(null=True)
    source = models.CharField(max_length=50, default='')
    abrev = models.CharField(max_length=50, default='')
    year = models.IntegerField(null=True)
    num_species = models.IntegerField(null=True)
    num_hybrid  = models.IntegerField(null=True)
    num_synonym  = models.IntegerField(null=True)
    num_spcimage = models.IntegerField(null=True, blank=True)
    num_spc_with_image = models.IntegerField(null=True, blank=True)
    pct_spc_with_image = models.DecimalField(decimal_places=2, max_digits=7,null=True, blank=True)
    num_hybimage = models.IntegerField(null=True, blank=True)
    num_hyb_with_image = models.IntegerField(null=True, blank=True)
    pct_hyb_with_image = models.DecimalField(decimal_places=2, max_digits=7,null=True, blank=True)
    notepad = models.CharField(max_length=500, default='')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pid

    def fullname(self):
        fname = self.genus
        if self.author:
            fname = fname + self.author
        if self.year:
            fname = fname + ' ' + self.year
        return fname

    def get_status(self):
        return self.status

    def get_description(self):
        return self.description

    def getAccepted(self):
        if 'synonym' in self.status:
            acc_id = Gensyn.objects.get(pid=self.pid).acc_id
            gen = Genus.objects.get(pid=acc_id)
            return "%s <i>%s</i>" % (gen.genus, gen.author)

    def getAcc(self):
        if 'synonym' in self.status:
            acc_id = Gensyn.objects.get(pid=self.pid).acc_id
            if acc_id:
                gen = Genus.objects.get(pid=acc_id)
                return gen.genus
            else:
                return "No accepted name found for this synonym."


    def getGenid(self):
        if 'synonym' in self.status:
            syn = Gensyn.objects.get(pid=self.pid).acc_id
            return "%s" % syn

    def getSynAuth(self):
        if 'synonym' in self.status:
            syn = Gensyn.objects.get(pid=self.pid).acc_author
            return "%s" % syn

    def get_roundspcpct(self):
        if self.pct_spc_with_image > 0:
            return round(self.pct_spc_with_image)
        else: return None

    def get_roundhybpct(self):
        if self.pct_hyb_with_image > 0:
            return round(self.pct_hyb_with_image)
        else: return None


    class Meta:
        # verbose_name_plural = "Anni"
        ordering = ('genus',)


class Genussyn(models.Model):
    pid = models.IntegerField(primary_key=True)
    acc = models.ForeignKey(Genus, verbose_name='genus', related_name='gen_syn', null=True,on_delete=models.DO_NOTHING)
    is_hybrid = models.CharField(max_length=1, null=True)
    genus = models.CharField(max_length=50, default='')
    author = models.CharField(max_length=200, default='')
    citation = models.CharField(max_length=200, default='')
    type = models.CharField(max_length=20, default='')
    distribution = models.TextField(null=True)
    text_data = models.TextField(null=True)
    source = models.CharField(max_length=50, default='')
    abrev = models.CharField(max_length=50, default='')
    year = models.IntegerField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.genus


class Gensyn(models.Model):
    pid = models.OneToOneField(
        Genus,
        db_column='pid',
        on_delete=models.DO_NOTHING,
        primary_key=True)
    accepted = models.CharField(max_length=50, default='')
    acc_author = models.CharField(max_length=50, default='')
    acc_year = models.IntegerField(null=True)
    status = models.CharField(max_length=20, default='')
    type = models.CharField(max_length=20, default='')
    description = models.CharField(max_length=255, default='')
    source = models.CharField(max_length=50, default='')
    abrev = models.CharField(max_length=50, default='')
    acc = models.ForeignKey(Genus, verbose_name='genus', related_name='gen_id', null=True,on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pid

        # def get_genid(self):
        # return self.acc_id


# TODO: Remove genus foreign keys from all intragen classes since these intregen classes are not unique by genus.
class Subgenus(models.Model):
    pid         = models.IntegerField(null=True)
    subgen      = models.IntegerField(default=0, db_column='subgen')
    subgenus    = models.CharField(primary_key=True, max_length=50, unique=True)
    author      = models.CharField(max_length=200, null=True)
    citation    = models.CharField(max_length=200, null=True)
    year        = models.IntegerField(null=True)
    description = models.TextField(null=True)
    distribution = models.TextField(null=True)
    gen         = models.ForeignKey(Genus, null=True, db_column='gen',on_delete=models.DO_NOTHING)
    genus = models.CharField(max_length=50, null=True)
    source = models.CharField(max_length=50, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subgenus
    class Meta:
        ordering = ['subgen']


class Section(models.Model):
    pid     = models.IntegerField(null=True)
    sec     = models.IntegerField(default=0, db_column='sec')
    section = models.CharField(primary_key=True, max_length=50, unique=True)
    subgenus = models.ForeignKey(Subgenus, null=True, db_column='subgenus',on_delete=models.DO_NOTHING)
    author  = models.CharField(max_length=200, null=True)
    citation = models.CharField(max_length=200, null=True)
    year    = models.IntegerField(null=True)
    description = models.TextField(null=True)
    distribution = models.TextField(blank=True)
    gen         = models.ForeignKey(Genus, null=True, db_column='gen',on_delete=models.DO_NOTHING)
    genus = models.CharField(max_length=50, null=True)
    source = models.CharField(max_length=50, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.section
    class Meta:
        ordering = ['section']


class Subsection(models.Model):
    pid         = models.IntegerField(null=True)
    subsec      = models.IntegerField(default=None, db_column='subsec')
    subgenus = models.ForeignKey(Subgenus, null=True, db_column='subgenus',on_delete=models.DO_NOTHING)
    section     = models.ForeignKey(Section, null=True, db_column='section',on_delete=models.DO_NOTHING)
    subsection  = models.CharField(primary_key=True, max_length=50, unique=True)
    author      = models.CharField(max_length=200, null=True)
    citation    = models.CharField(max_length=200, null=True)
    year        = models.IntegerField(null=True)
    description = models.TextField(null=True)
    sec         = models.IntegerField(Section, null=True, default=None, db_column='sec')
    distribution = models.TextField(null=True)
    gen         = models.ForeignKey(Genus, null=True, db_column='gen',on_delete=models.DO_NOTHING)
    genus = models.CharField(max_length=50)
    source = models.CharField(max_length=50,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subsection
    class Meta:
        ordering = ['subsection']


class Series(models.Model):
    pid     = models.IntegerField(null=True)
    ser     = models.IntegerField(default='', db_column='ser')
    subgenus = models.ForeignKey(Subgenus, null=True, db_column='subgenus',on_delete=models.DO_NOTHING)
    section     = models.ForeignKey(Section, null=True, db_column='section',on_delete=models.DO_NOTHING)
    subsection     = models.ForeignKey(Subsection, null=True,db_column='subsection',on_delete=models.DO_NOTHING)
    series  = models.CharField(primary_key=True,max_length=50, unique=True)
    author  = models.CharField(max_length=200, null=True)
    citation    = models.CharField(max_length=200, null=True)
    year    = models.IntegerField(null=True)
    description = models.TextField(null=True)
    distribution = models.TextField(null=True)
    gen         = models.ForeignKey(Genus, null=True, db_column='gen',on_delete=models.DO_NOTHING)
    genus = models.CharField(max_length=50, null=True)
    source = models.CharField(max_length=50, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.series
    class Meta:
        ordering = ['series']


class GenusTree(MPTTModel):
    genus    = models.CharField(max_length=50, unique=True)
    parent      = TreeForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['pid_pair']

    def getpid(self):
        pid, par = self.pid_pair.split('|')
        return pid


class Alliance(models.Model):
    class Meta:
        unique_together = (("alid", "gen"),)
        ordering = ['alliance']

    alid = models.ForeignKey(Genus, db_column='alid', related_name='alid', null=True, blank=True,on_delete=models.DO_NOTHING)
    gen = models.ForeignKey(Genus, db_column='gen', related_name='algen', null=True, blank=True,on_delete=models.DO_NOTHING)
    alliance = models.CharField(max_length=50)
    type = models.CharField(max_length=10)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.alliance


class Infragen (models.Model):
    # class Meta:
    #     unique_together = (("genus", "infragen","rank","author"),)
    source_pid = models.IntegerField(default=0)
    version  = models.IntegerField(default=1)
    gen      = models.ForeignKey(Genus,db_column='gen',null=True,on_delete=models.DO_NOTHING)
    genus    = models.CharField(max_length=50, null=True)
    infragen = models.CharField(max_length=50)
    rank     = models.CharField(max_length=10)
    author   = models.CharField(max_length=200, null=True)
    citation = models.CharField(max_length=200, null=True)
    year     = models.IntegerField(null=True)
    source   = models.CharField(max_length=50,null=True)
    description = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Infragenrelation (models.Model):
    gen      = models.ForeignKey(Genus,db_column='gen',on_delete=models.DO_NOTHING)
    genus    = models.CharField(max_length=50, null=True)
    infragen = models.CharField(max_length=50)
    parent   = models.ForeignKey(Infragen,null=True, db_column='parent_pid',on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Intragen (models.Model):
    class Meta:
        unique_together = (("gen", "subgen","sec","subsec","ser"),)
    gen     = models.ForeignKey(Genus,db_column='gen',on_delete=models.DO_NOTHING)
    subgen  = models.IntegerField(db_column='subgen',null=True, blank=True)
    sec     = models.IntegerField(db_column='sec',null=True, blank=True)
    subsec  = models.IntegerField(db_column='subsec',null=True, blank=True)
    ser     = models.IntegerField(db_column='ser',null=True, blank=True)
    type_status = models.CharField(max_length=20, blank=True)
    genus   = models.CharField(max_length=50, blank=True)
    subfamily = models.ForeignKey(Subfamily, null=True, default='', db_column='subfamily',on_delete=models.DO_NOTHING)
    tribe  = models.ForeignKey(Tribe, null=True, default='', db_column='tribe',on_delete=models.DO_NOTHING)
    subtribe  = models.ForeignKey(Subtribe, null=True, default='', db_column='subtribe',on_delete=models.DO_NOTHING)
    subgenus  = models.ForeignKey(Subgenus, null=True,db_column='subgenus',on_delete=models.DO_NOTHING)
    section   = models.ForeignKey(Section, null=True,db_column='section',on_delete=models.DO_NOTHING)
    subsection= models.ForeignKey(Subsection, null=True,db_column='subsection',on_delete=models.DO_NOTHING)
    series   = models.ForeignKey(Series, null=True,db_column='series',on_delete=models.DO_NOTHING)
    # subgenus  = models.CharField(max_length=50, blank=True)
    # section   = models.CharField(max_length=50, blank=True)
    # subsection= models.CharField(max_length=50, blank=True)
    # series   = models.CharField(max_length=50, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Species(models.Model):
    pid = models.IntegerField(primary_key=True)
    source = models.CharField(max_length=10)
    genus = models.CharField(max_length=50)
    is_hybrid = models.CharField(max_length=1, null=True)
    species = models.CharField(max_length=50)
    infraspr = models.CharField(max_length=20, null=True)
    infraspe = models.CharField(max_length=50, null=True)
    author = models.CharField(max_length=200)
    originator = models.CharField(max_length=100, blank=True)
    citation = models.CharField(max_length=200)
    cit_status = models.CharField(max_length=20, null=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='')
    type = models.CharField(max_length=10,choices=TYPE_CHOICES,default='')
    year = models.IntegerField(null=True)
    date = models.DateField(null=True)
    distribution = models.TextField(blank=True)
    physiology = models.CharField(max_length=200, blank=True)
    url = models.CharField(max_length=200, blank=True)
    url_name = models.CharField(max_length=100, blank=True)
    num_image = models.IntegerField(blank=True)
    num_ancestor = models.IntegerField(null=True, blank=True)
    num_species_ancestor = models.IntegerField(null=True, blank=True)
    num_descendant = models.IntegerField(null=True, blank=True)
    num_dir_descendant = models.IntegerField(null=True, blank=True)
    gen = models.ForeignKey(Genus, db_column='gen', default=0,on_delete=models.DO_NOTHING)
    notepad = models.CharField(max_length=500, default='')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)

    # TODO: add reference column
    def __str__(self):
        name = self.species
        if self.infraspr:
            name = '%s %s %s' % (name, self.infraspr, self.infraspe)
        return name

    def speciesname(self):
        if self.type == 'species' or self.is_hybrid:
            spc = '<i>%s</i>' % self.species
            if self.is_hybrid:
                spc = '%s %s' % (self.is_hybrid, spc)
        elif self.type == 'hybrid':
            spc = re.sub('Memoria', 'Mem.', self.species.rstrip())
        else:
            spc = '<i>%s</i>' % self.species

        if self.infraspr:
            spc = '%s %s <i>%s</i>' % (spc, self.infraspr, self.infraspe)
        return spc

    def fullspeciesname(self):
        if self.type == 'species' or self.is_hybrid:
            spc = '<i>%s</i>' % self.species
            if self.is_hybrid:
                spc = '%s %s' % (self.is_hybrid, spc)
        else:
            spc = '<i>%s</i>' % self.species

        if self.infraspr:
            spc = '%s %s <i>%s</i>' % (spc, self.infraspr, self.infraspe)

        return spc

    def textspeciesname(self):
        spc = re.sub('Memoria', 'Mem.', self.species.rstrip())
        if self.infraspr:
            spc = '%s %s %s' % (self.species, self.infraspr, self.infraspe)
        if self.is_hybrid:
            spc = '%s %s' % (self.is_hybrid, spc)
        return spc

    def textspeciesnamefull(self):
        spc = self.species.rstrip()
        if self.infraspr:
            spc = '%s %s %s' % (self.species, self.infraspr, self.infraspe)
        if self.is_hybrid:
            spc = '%s %s' % (self.is_hybrid, spc)
        return spc

    def shortspeciesname(self):
        return '%s %s' % (self.genus, self.species)

    def textname(self):
        return '%s %s' % (self.genus, self.textspeciesname())

    def name(self):
        return '<i>%s</i> %s' % (self.genus, self.speciesname())

    def abrevname(self):
        return '<i>%s</i> %s' % (self.gen.abrev, self.speciesname())

    def namecasual(self):
        namecasual = self.abrevname()
        namecasual = re.sub('Memoria', 'Mem.', namecasual.rstrip())
        return namecasual

    def navbar_name(self):
        # name = self.speciesname()
        name = self.species
        if self.infraspr:
            name = name + ' ' + self.infraspr + ' ' + self.infraspe
        if self.is_hybrid:
            name = name + " (" + self.is_hybrid
            if self.year:
                name = name + " " + str(self.year)
            if self.num_image > 0:
                name = name + " #img " + str(self.num_image)
            return name + ")"
        elif self.year:
            name = name + " (" + str(self.year)
            if self.status == 'synonym':
                name = name + " syn"
            elif self.num_image and self.num_image > 0:
                name = name + " #img " + str(self.num_image)
            return name + ")"
        return name

    def get_species(self):
        name = '%s' % (self.species)
        # if self.is_hybrid:
        #     name = '%s %s' % (self.is_hybrid, name)
        if self.infraspr:
            name = '%s %s %s' % (name, self.infraspr, self.infraspe)
        return name

    def getAccepted(self):
        if 'synonym' in self.status:
            return Synonym.objects.get(pk=self.pid).acc
        return None

    def getAcc(self):
        if self.status == 'synonym':
            spid = Synonym.objects.get(spid=self.pid)
            return spid.acc_id
        return "Not a synonym."

    def getAbrevName(self):
        name = self.species
        name = re.sub('Memoria', 'Mem.', name.rstrip())
        if self.gen.abrev:
            if self.infraspe:
                name = self.gen.abrev + ' '+ name + ' ' + self.infraspr + ' ' + self.infraspe
            else:
                name = self.gen.abrev + ' '+ name
        else:
            name = self.name()
        return name

    def grex(self):
        if self.infraspe:
            return str(self.genus) + ' ' + str(self.species) + ' ' + str(self.infraspr) + ' ' + str(self.infraspe)
        else:
            return str(self.genus) + ' ' + str(self.species)

    def short_grex(self):
        if self.infraspe:
            return str(self.species) + ' ' + str(self.infraspr) + ' ' + str(self.infraspe)
        else:
            return str(self.species)

    def sourceurl(self):
        if self.source == 'Kew':
            return "https://wcsp.science.kew.org/namedetail.do?name_id=" + str(self.pid)
        elif self.source == 'RHS':
            return "http://apps.rhs.org.uk/horticulturaldatabase/orchidregister/orchiddetails.asp?ID=" + str(self.pid - 100000000)
        else:
            return "#"

    def get_best_img(self):
        if self.type == 'species':
            img = SpcImages.objects.filter(pid=self.pid).filter(image_file__isnull=False).filter(rank__lt=7).order_by('quality','-rank','?')
        else:
            img = HybImages.objects.filter(pid=self.pid).filter(image_file__isnull=False).filter(rank__lt=7).order_by('quality','-rank', '?')
            
        if img.count()>0:
            img = img[0:1][0]
            return img
        return None

    def get_best_img_by_author(self,author):
        if self.type == 'species':
            img = SpcImages.objects.filter(pid=self.pid).filter(author_id=author).filter(image_file__isnull=False).filter(rank__lt=7).order_by(
                'quality', '-rank', '?')
        else:
            img = HybImages.objects.filter(pid=self.pid).filter(author_id=author).filter(image_file__isnull=False).filter(rank__lt=7).order_by(
                'quality', '-rank', '?')

        if img.count() > 0:
            img = img[0:1][0]
            return img
        return None


class Specieshistory(models.Model):
    pid = models.ForeignKey(Species,db_column='pid', on_delete=models.CASCADE)
    genus = models.CharField(max_length=50, null=True)
    species = models.CharField(max_length=100, null=True)
    infraspr = models.CharField(max_length=20, null=True)
    infraspe = models.CharField(max_length=50, null=True)
    source = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    status = models.CharField(max_length=20)
    is_active = models.BooleanField(null=True,default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, blank=False)
    pid = models.ForeignKey(Species, on_delete=models.CASCADE, related_name='comm_pid')
    reason = models.CharField(max_length=20, blank=False)
    memo = models.TextField(max_length=500, blank=True)
    id_list = models.CharField(max_length=200, blank=True)
    # relevancy = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        # user = self.user
        # mypid = self.pid
        return self.pid


class SpeciesDetail (models.Model):
    pid = models.OneToOneField(
        Species,
        db_column='pid',
        on_delete=models.DO_NOTHING,
        primary_key=True)
    url = models.CharField(max_length=200, blank=True)
    url_name = models.CharField(max_length=100, blank=True)
    common_name = models.CharField(max_length=100, blank=True)
    local_name = models.CharField(max_length=100, blank=True)
    avg_size        = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)
    stem            = models.CharField(max_length=500, blank=True)
    leaf            = models.CharField(max_length=500, blank=True)
    inflorescence   = models.CharField(max_length=500, blank=True)
    flower          = models.CharField(max_length=500, blank=True)
    sepal           = models.CharField(max_length=500, blank=True)
    mentum          = models.CharField(max_length=500, blank=True)
    petal           = models.CharField(max_length=500, blank=True)
    lip             = models.CharField(max_length=500, blank=True)
    fragrance       = models.CharField(max_length=500, blank=True)
    habitat         = models.CharField(max_length=500, blank=True)
    altitude = models.CharField(max_length=500, blank=True)
    bloom_period    = models.CharField(max_length=50, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s %s %s' % (self.genus, self.species,
                                self.infraspr, self.infraspe)


class Culture (models.Model):
    pid = models.OneToOneField(
        Species,
        db_column='pid',
        on_delete=models.DO_NOTHING,
        primary_key=True)
    temperature     = models.CharField(max_length=100, blank=True)
    light           = models.CharField(max_length=100, blank=True)
    water           = models.CharField(max_length=100, blank=True)
    winter_care     = models.CharField(max_length=100, blank=True)
    bloom_month     = models.CharField(max_length=50, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s %s %s' % (self.genus, self.species,
                                self.infraspr, self.infraspe)


class Similarity (models.Model):
    class Meta:
        unique_together = (("pid1", "pid2"),)
    pid1            = models.ForeignKey(Species,db_column='pid1', related_name='pid1',on_delete=models.DO_NOTHING)
    pid2            = models.ForeignKey(Species,db_column='pid2', related_name='pid2',on_delete=models.DO_NOTHING)
    differences     = models.TextField(blank=True)
    similar         = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class NewAcceptedManager(models.Manager):
    def get_queryset(self):
        return super(NewAcceptedManager, self).get_queryset().filter(status='NEW')


class Accepted(models.Model):
    pid = models.OneToOneField(
        Species,
        db_column='pid',
        on_delete=models.CASCADE,
        primary_key=True)
    gen = models.ForeignKey(Genus, db_column='gen', null=True, blank=True,on_delete=models.DO_NOTHING)
    genus = models.CharField(max_length=50)
    species = models.CharField(max_length=50)
    infraspr = models.CharField(max_length=20, null=True)
    infraspe = models.CharField(max_length=50, null=True)
    is_hybrid = models.CharField(max_length=1, null=True)
    distribution = models.TextField(blank=True)
    is_type = models.BooleanField(null=True, default=False)
    physiology = models.CharField(max_length=200, null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    url_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    common_name = models.CharField(max_length=100, null=True, blank=True)
    local_name = models.CharField(max_length=100, null=True, blank=True)
    bloom_month = models.CharField(max_length=200, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    fragrance = models.CharField(max_length=50, null=True, blank=True)
    altitude = models.CharField(max_length=50, null=True, blank=True)

    history = models.TextField(null=True, blank=True)
    analysis = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    etymology  = models.TextField(null=True, blank=True)
    culture  = models.TextField(null=True, blank=True)

    subgenus = models.ForeignKey(Subgenus, db_column='subgenus', null=True,on_delete=models.DO_NOTHING)
    section = models.ForeignKey(Section, db_column='section', null=True,on_delete=models.DO_NOTHING)
    subsection = models.ForeignKey(Subsection, db_column='subsection', null=True,on_delete=models.DO_NOTHING)
    series = models.ForeignKey(Series, db_column='series', null=True,on_delete=models.DO_NOTHING)
    intrasource = models.CharField(max_length=10)

    num_image = models.IntegerField(null=True, blank=True)
    num_descendant = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    operator = models.ForeignKey(User, db_column='operator', null=True,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.pid.name()

# Collection of intrageneric placements from diverse sources. May contain naturakl hybrid
class Infragenspc (models.Model):
    class Meta:
        unique_together = (("pid", "subgenus","section","subsection","series"),)
    pid     = models.ForeignKey(Species,db_column='pid',on_delete=models.DO_NOTHING)
    author = models.CharField(max_length=200)
    citation = models.CharField(max_length=200)
    source = models.CharField(max_length=10)
    gen     = models.ForeignKey(Genus,db_column='gen',on_delete=models.DO_NOTHING)
    genus   = models.CharField(max_length=50, null=True, default=None)
    species = models.CharField(max_length=50, null=True, default=None)
    infraspr = models.CharField(max_length=20, null=True, default=None)
    infraspe = models.CharField(max_length=50, null=True, default=None)
    subgenus  = models.ForeignKey(Subgenus, null=True,db_column='subgenus',on_delete=models.DO_NOTHING)
    section   = models.ForeignKey(Section, null=True,db_column='section',on_delete=models.DO_NOTHING)
    subsection= models.ForeignKey(Subsection, null=True,db_column='subsection',on_delete=models.DO_NOTHING)
    series   = models.ForeignKey(Series, null=True,db_column='series',on_delete=models.DO_NOTHING)
    certainty = models.BooleanField(null=True, default=True)
    # subgenus  = models.CharField(max_length=50, blank=True, default=None)
    # section   = models.CharField(max_length=50, blank=True, default=None)
    # subsection= models.CharField(max_length=50, blank=True, default=None)
    # series   = models.CharField(max_length=50, blank=True, default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Synonym(models.Model):
    spid = models.OneToOneField(
        Species,
        related_name='spid',
        db_column='spid',
        on_delete=models.CASCADE,
        primary_key=True)
    acc = models.ForeignKey(Species, verbose_name='accepted genus',related_name='accid',on_delete=models.DO_NOTHING)
    gen = models.ForeignKey(Genus, db_column='gen', related_name='gen', null=True, blank=True,on_delete=models.DO_NOTHING)
    year = models.IntegerField(null=True, blank=True)
    genus = models.CharField(max_length=50, null=True, blank=True)
    is_hybrid = models.CharField(max_length=5, null=True, blank=True)
    species = models.CharField(max_length=50, null=True, blank=True)
    infraspr = models.CharField(max_length=20, null=True, blank=True)
    infraspe = models.CharField(max_length=50, null=True, blank=True)
    sgen = models.ForeignKey(Genus, db_column='sgen', related_name='sgen', null=True, blank=True,on_delete=models.DO_NOTHING)
    syear = models.IntegerField(null=True, blank=True)
    sgenus = models.CharField(max_length=50, null=True, blank=True)
    sis_hybrid = models.CharField(max_length=5, null=True, blank=True)
    sspecies = models.CharField(max_length=50, null=True, blank=True)
    sinfraspr = models.CharField(max_length=20, null=True, blank=True)
    sinfraspe = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=10, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.spid.name()

    def get_shortname(self):
        if self.sis_hybrid:
            if self.sinfraspe:
                return '%s %s %s %s %s' % (self.sgenus, self.sis_hybrid, self.sspecies,
                                           self.sinfraspr, self.sinfraspe)
            else:
                return '%s %s %s' % (self.sgenus, self.sis_hybrid, self.sspecies)
        else:
            if self.sinfraspe:
                return '%s %s %s %s' % (self.sgenus, self.sspecies,
                                        self.sinfraspr, self.sinfraspe)
            else:
                return '%s %s' % (self.sgenus, self.sspecies)

    def get_abrevname(self):
        abrev = self.sgen.abrev
        if not abrev:
            abrev = self.sgen.genus
        if self.sis_hybrid:
            if self.sinfraspe:
                return '%s %s %s %s %s' % (abrev, self.sis_hybrid, self.sspecies,
                                           self.sinfraspr, self.sinfraspe)
            else:
                return '%s %s %s' % (abrev, self.sis_hybrid, self.sspecies)
        else:
            if self.sinfraspe:
                return '%s %s %s %s' % (abrev, self.sspecies,
                                        self.sinfraspr, self.sinfraspe)
            else:
                return '%s %s' % (abrev, self.sspecies)

    def get_shortaccepted(self):
        if self.is_hybrid:
            if self.infraspe:
                return '%s %s %s %s %s' % (self.genus, self.is_hybrid, self.species, self.infraspr, self.infraspe)
            else:
                return '%s %s %s' % (self.genus, self.is_hybrid, self.species)
        else:
            if self.infraspe:
                return '%s %s %s %s' % (self.genus, self.species, self.infraspr, self.infraspe)
            else:
                return '%s %s' % (self.genus, self.species)


class Hybrid(models.Model):
    # pid                 = models.IntegerField(db_column='pid',primary_key=True)
    pid = models.OneToOneField(
        Species,
        db_column='pid',
        on_delete=models.DO_NOTHING,
        primary_key=True)
    gen = models.ForeignKey(Genus, db_column='gen', default=0, on_delete=models.DO_NOTHING)
    source = models.CharField(max_length=10, null=True, blank=True)
    genus = models.CharField(max_length=50, null=True, blank=True)
    species = models.CharField(max_length=50, null=True, blank=True)
    infraspr = models.CharField(max_length=20, null=True, blank=True)
    is_hybrid = models.CharField(max_length=5, null=True, blank=True)
    hybrid_type = models.CharField(max_length=20, null=True, blank=True)
    infraspe = models.CharField(max_length=50, null=True, blank=True)
    author = models.CharField(max_length=200, null=True, blank=True)
    seed_gen = models.ForeignKey(Genus, db_column='seedgen', related_name='seedgen', null=True, on_delete=models.DO_NOTHING)
    seed_genus = models.CharField(max_length=50, null=True, blank=True)
    seed_species = models.CharField(max_length=50, null=True, blank=True)
    seed_type = models.CharField(max_length=10, null=True, blank=True)
    seed_id = models.ForeignKey(Species,db_column='seed_id',related_name='seed_id',null=True, blank=True,on_delete=models.DO_NOTHING)
    pollen_gen = models.ForeignKey(Genus, db_column='pollgen', related_name='pollgen',null=True, on_delete=models.DO_NOTHING)
    pollen_genus = models.CharField(max_length=50, null=True, blank=True)
    pollen_species = models.CharField(max_length=50, null=True, blank=True)
    pollen_type = models.CharField(max_length=10, null=True, blank=True)
    pollen_id = models.ForeignKey(Species,db_column='pollen_id',related_name='pollen_id',null=True, blank=True,on_delete=models.DO_NOTHING)
    year = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    originator = models.CharField(max_length=100, null=True, blank=True)
    user_id = models.ForeignKey(User, db_column='user_id', null=True, blank=True,on_delete=models.DO_NOTHING)

    description = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    history = models.TextField(null=True, blank=True)
    culture = models.TextField(null=True, blank=True)
    etymology = models.TextField(null=True, blank=True)

    num_image = models.IntegerField(null=True, blank=True)
    num_ancestor = models.IntegerField(null=True, blank=True)
    num_species_ancestor = models.IntegerField(null=True, blank=True)
    num_descendant = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pid.name()

    def registered_seed_name(self):
        name = self.seed_id.name()
        if self.seed_id.textspeciesnamefull() != self.seed_species or self.seed_id.genus != self.seed_genus:
            name = self.seed_genus + ' ' + self.seed_species + ' ' + '(syn)'
        return name

    def registered_seed_name_short(self):
        name = self.seed_id.abrevname()
        if self.seed_id.textspeciesnamefull() != self.seed_species or self.seed_id.genus != self.seed_genus:
            name = self.seed_genus + ' ' + self.seed_species + ' ' + '(syn)'
        return name

    # Used in hybrid-detail parents
    def registered_pollen_name(self):
        name = self.pollen_id.name()
        if self.pollen_id.textspeciesnamefull() != self.pollen_species or self.pollen_id.genus != self.pollen_genus:
            name = self.pollen_genus + ' ' + self.pollen_species + ' ' + '(syn)'
        return name

    def registered_pollen_name_short(self):
        name = self.pollen_id.abrevname()
        if self.pollen_id.textspeciesnamefull() != self.pollen_species or self.pollen_id.genus != self.pollen_genus:
            name = self.pollen_genus + ' ' + self.pollen_species + ' ' + '(syn)'
        return name

    def registered_seed_name_long(self):
        name = self.seed_id.name()
        if self.seed_id.textspeciesnamefull() != self.seed_species or self.seed_id.genus != self.seed_genus:
            name = self.seed_genus + ' ' + self.seed_species + ' ' + '(syn ' + self.seed_id.textname() + ')'
        return name

    def registered_pollen_name_long(self):
        name = self.pollen_id.name()
        if self.pollen_id.textspeciesnamefull() != self.pollen_species or self.pollen_id.genus != self.pollen_genus:
            name = self.pollen_genus + ' ' + self.pollen_species + ' ' + '(syn ' + self.pollen_id.textname() + ')'
        return name


    # def registered_seed_name_long(self):
    #     name = self.seed_genus + ' ' + self.seed_species
    #     if self.seed_id.textspeciesname() != self.seed_species or self.seed_id.genus != self.seed_genus:
    #         name = name + ' ' + '(syn ' + self.seed_id.textname() + ')'
    #     name = '<i>' + name + '</i>'
    #     return name
    #
    # # Used in hybrid_detail/parents name
    # def registered_pollen_name_long(self):
    #     name = self.pollen_genus + ' ' + self.pollen_species
    #     if self.pollen_id.textspeciesname() != self.pollen_species or self.pollen_id.genus != self.pollen_genus:
    #         name = name + ' ' + '(syn ' + self.pollen_id.textname() + ')'
    #     name = '<i>' + name + '</i>'
    #     return name

    def seed_status(self):
        if self.seed_id and self.seed_id.textname() != self.seed_genus + ' ' + self.seed_species:
            return 'syn'
        return None

    def pollen_status(self):
        if self.pollen_id and self.pollen_id.textname() != self.pollen_genus + ' ' + self.pollen_species:
            return 'syn'
        return None

    def hybrid_type(self):
        if self.is_hybrid:
            return 'natural'
        else:
            return 'artificial'


class InfragenHybrid(models.Model):
    pid = models.OneToOneField(
        Species,
        db_column='pid',
        on_delete=models.DO_NOTHING,
        primary_key=True)
    genus = models.CharField(max_length=50, null=True, blank=True)
    species = models.CharField(max_length=50, null=True, blank=True)
    subfamily   = models.CharField(max_length=500, null=True, blank=True)
    tribe       = models.CharField(max_length=500, null=True, blank=True)
    subtribe    = models.CharField(max_length=500, null=True, blank=True)
    subgenus    = models.CharField(max_length=500, null=True, blank=True)
    section     = models.CharField(max_length=500, null=True, blank=True)
    subsection  = models.CharField(max_length=500, null=True, blank=True)
    series      = models.CharField(max_length=500, null=True, blank=True)
    sf_pct      = models.CharField(max_length=500, null=True, blank=True)
    t_pct       = models.CharField(max_length=500, null=True, blank=True)
    st_pct      = models.CharField(max_length=500, null=True, blank=True)
    subgen_pct  = models.CharField(max_length=500, null=True, blank=True)
    sec_pct     = models.CharField(max_length=500, null=True, blank=True)
    subsec_pct  = models.CharField(max_length=500, null=True, blank=True)
    ser_pct     = models.CharField(max_length=500, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return '%s' % (self.pid)


class AncestorDescendant(models.Model):
    class Meta:
        unique_together = (("did", "aid"),)

    did = models.ForeignKey(Hybrid, null=False, db_column='did',on_delete=models.CASCADE)
    aid = models.ForeignKey(Species, null=False, db_column='aid',on_delete=models.DO_NOTHING)
    anctype = models.CharField(max_length=10, default='hybrid')
    pct = models.FloatField(blank=True, null=True)
    # file = models.CharField(max_length=10, blank=True)

    def __str__(self):
        hybrid = '%s %s' % (self.did.genus, self.did.species)
        pct = '%'
        return '%s %s %s' % (hybrid, self.aid, self.pct)

    def anc_name(self):
        name = Species.objects.get(pk=self.aid.pid)
        if name.infraspr:
            return "%s %s %s %s" % (name.genus, name.species, name.infraspr,name.infraspe)
        else:
            return "%s %s" % (name.genus, name.species)

    def anc_abrev(self):
        # name = Species.objects.get(pk=self.aid.pid)
        abrev = self.did.abrev
        return self.did.nameabrev()

    def prettypct(self):
        # pct = int(self.pct*100)/100
        percent = '{:5.2f}'.format(float(self.pct))

        return percent.strip("0").strip(".")


class TestUploadFile(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    user_id    = models.ForeignKey(User, db_column='user_id', null=True, blank=True,on_delete=models.DO_NOTHING)
    image_file_path = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name


class UploadFile(models.Model):
    pid        = models.ForeignKey(Species, null=True, blank=True, db_column='pid',on_delete=models.DO_NOTHING)
    author     = models.ForeignKey(Photographer, db_column='author', null=True, blank=True,on_delete=models.DO_NOTHING)
    user_id    = models.ForeignKey(User, db_column='user_id', null=True, blank=True,on_delete=models.DO_NOTHING)
    credit_to  = models.CharField(max_length=100, null=True, blank=True)    #should match author_id inPhotography
    source_url = models.CharField(max_length=1000, null=True, blank=True)
    source_file_name = models.CharField(max_length=100, null=True, blank=True)
    name        = models.CharField(max_length=100, null=True, blank=True)
    awards      = models.CharField(max_length=200, null=True, blank=True)
    variation   = models.CharField(max_length=50, null=True, blank=True)
    forma       = models.CharField(max_length=50, null=True, blank=True)
    originator  = models.CharField(max_length=50, null=True, blank=True)
    text_data   = models.TextField(null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    certainty   = models.CharField(max_length=20, null=True, blank=True)
    type        = models.CharField(max_length=20, null=True, blank=True)
    location    = models.CharField(max_length=100, null=True, blank=True)
    rank        = models.IntegerField(choices=RANK_CHOICES,default=0)
    image_file_path = models.ImageField(upload_to='images/', null=True, blank=True)
    image_file  = models.CharField(max_length=100, null=True, blank=True)
    is_private  = models.BooleanField(null=True, default=False)
    compressed  = models.BooleanField(null=True, default=False)
    block_id    = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pid.name()


@receiver(post_save, sender=UploadFile, dispatch_uid="update_image_profile")
def update_image(sender, instance, **kwargs):
    if instance.image_file_path:
        fullpath = settings.MEDIA_ROOT + '/' + str(instance.image_file_path)
        rotate_image(fullpath)


class SpcImages(models.Model):
    pid = models.ForeignKey(Accepted, null=False, db_column='pid',on_delete=models.DO_NOTHING)
    author = models.ForeignKey(Photographer, db_column='author', on_delete=models.DO_NOTHING)
    credit_to = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=10, default='TBD')
    quality = models.IntegerField(
                               choices=QUALITY,
                               default=3,
                               )
    name = models.CharField(max_length=100, null=True, blank=True)
    source_url = models.CharField(max_length=1000, null=True, blank=True)
    image_url = models.CharField(max_length=500, null=True, blank=True)
    text_data = models.TextField(null=True, blank=True)
    certainty = models.CharField(max_length=20, null=True, blank=True)
    rank = models.IntegerField(choices=RANK_CHOICES,default=5)
    zoom = models.IntegerField(default=0)
    form = models.CharField(max_length=50, null=True, blank=True)
    source_file_name = models.CharField(max_length=100, null=True, blank=True)
    spid = models.IntegerField(null=True, blank=True)
    awards = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    variation = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)
    # width = models.FloatField(default=1)
    # height = models.FloatField(default=1)
    image_file = models.CharField(max_length=100, null=True, blank=True)
    image_file_path = models.ImageField(upload_to='utils/images/photos', null=True, blank=True)
    download_date = models.DateField(null=True, blank=True)
    # gen = models.ForeignKey(Genus, null=True, blank=True, db_column='gen',on_delete=models.DO_NOTHING)
    # gen = models.IntegerField(null=True, blank=True)
    gen = models.ForeignKey(Genus, db_column='gen', null=True, blank=True,on_delete=models.DO_NOTHING)
    is_private = models.BooleanField(null=True, default=False)
    block_id = models.IntegerField(null=True, blank=True)
    user_id = models.ForeignKey(User, db_column='user_id', null=True, blank=True,on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    # upload_by = models.ForeignKey(User, db_column='upload_by', null=True, blank=True,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.pid.pid.textname()

    def imgname(self):
        if self.source_file_name:
            myname = '<i>%s</i>' % (self.source_file_name)
        else:
            myname = self.pid.pid.abrevname()
        if self.variation:
            myname = '%s %s ' % (myname, self.variation)
        if self.form:
            myname = '%s %s form ' % (myname, self.form)
        if self.certainty:
            myname = '%s %s ' % (myname, self.certainty)
        if self.name:
            myname = "%s '%s' " % (myname, self.name)
        if self.awards:
            myname = '%s %s' % (myname, self.awards)
        return myname

    def imginfo(self):
        myname = ''
        if self.variation:
            myname = '%s %s ' % (myname, self.variation)
        if self.form:
            myname = '%s %s form ' % (myname, self.form)
        if self.certainty:
            myname = '%s %s ' % (myname, self.certainty)
        if self.name:
            myname = "%s '%s' " % (myname, self.name)
        if self.awards:
            myname = '%s %s' % (myname, self.awards)
        return myname

    def fullimgname(self):
        if self.source_file_name:
            myname = self.source_file_name
        else:
            myname = self.pid.pid
        if self.variation:
            myname = '%s %s ' % (myname, self.variation)
        if self.form:
            myname = '%s %s form ' % (myname, self.form)
        if self.certainty:
            myname = '%s %s ' % (myname, self.certainty)
        if self.name:
            myname = "%s '%s' " % (myname, self.name)
        if self.awards:
            myname = '%s %s' % (myname, self.awards)
        return myname

    def abrev(self):
        return '%s' % Genus.objects.get(pk=self.gen_id).abrev

    def web(self):
        web = Photographer.objects.get(author_id=self.author)
        return web.web

    # TODO: add block_id
    def image_dir(self):
        return 'utils/images/species/'
        # return 'utils/images/hybrid/' + block_id + '/'

    def thumb_dir(self):
        return 'utils/images/species_thumb/'

    def get_displayname(self):
        if self.credit_to:
            return self.credit_to
        return self.author.displayname

    def get_userid(self):
        author = Photographer.objects.get(author=self.author_id)
        return author.user_id


class HybImages(models.Model):
    form = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    rank = models.IntegerField(choices=RANK_CHOICES,default=5)
    zoom = models.IntegerField(default=0)
    certainty = models.CharField(max_length=20, null=True, blank=True)
    source_file_name = models.CharField(max_length=100, null=True, blank=True)
    awards = models.CharField(max_length=200, null=True, blank=True)
    detail = models.CharField(max_length=20, null=True, blank=True)
    cultivator = models.CharField(max_length=50, null=True, blank=True)
    hybridizer = models.CharField(max_length=50, null=True, blank=True)
    author = models.ForeignKey(Photographer, db_column='author', on_delete=models.DO_NOTHING)
    credit_to = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=10, default='TBD')
    quality = models.IntegerField(
                               choices=QUALITY,
                               default=3,
                               )
    location = models.CharField(max_length=100, null=True, blank=True)
    source_url = models.CharField(max_length=1000, null=True, blank=True)
    image_url = models.CharField(max_length=500, null=True, blank=True)
    text_data = models.TextField(null=True, blank=True)
    description = models.CharField(max_length=400, null=True, blank=True)
    variation = models.CharField(max_length=50, null=True, blank=True)
    # width = models.FloatField(default=1)
    # height = models.FloatField(default=1)
    image_file = models.CharField(max_length=100, null=True, blank=True)
    image_file_path = models.ImageField(upload_to='utils/images/photos', null=True, blank=True)
    download_date = models.DateField(null=True, blank=True)
    pid = models.ForeignKey(Hybrid, db_column='pid', verbose_name='grex', null=True, blank=True,on_delete=models.DO_NOTHING)
    spid = models.IntegerField(null=True, blank=True)
    gen = models.ForeignKey(Genus, db_column='gen', null=True, blank=True,on_delete=models.DO_NOTHING)
    is_private = models.BooleanField(null=True, default=False)
    block_id = models.IntegerField(null=True, blank=True)
    user_id = models.ForeignKey(User, db_column='user_id', null=True, blank=True,on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    # upload_by = models.ForeignKey(User, db_column='upload_by', null=True, blank=True,on_delete=models.DO_NOTHING)

    def __str__(self):
        name = self.pid.pid.name()
        if self.variation:
            name = name + ' ' + self.variation
        if self.form:
            name = name + ' ' + self.form
        if self.name:
            name = name + ' ' + self.name
        if self.awards:
            name = name + ' ' + self.awards
        # return '%s %s %s' % (self.author_id, str(self.pid), self.image_file)
        return name

    def imginfo(self):
        myname = ''
        if self.variation:
            myname = '%s %s ' % (myname, self.variation)
        if self.form:
            myname = '%s %s form ' % (myname, self.form)
        if self.certainty:
            myname = '%s %s ' % (myname, self.certainty)
        if self.name:
            myname = "%s '%s' " % (myname, self.name)
        if self.awards:
            myname = '%s %s' % (myname, self.awards)
        return myname

    def imgname(self):
        if self.source_file_name:
            myname = self.source_file_name
        else:
            myname = self.pid.pid.abrevname()
        if self.variation:
            myname = '%s %s ' % (myname, self.variation)
        if self.form:
            myname = '%s %s form ' % (myname, self.form)
        if self.certainty:
            myname = '%s %s ' % (myname, self.certainty)
        if self.name:
            myname = "%s '%s' " % (myname, self.name)
        if self.awards:
            myname = '%s %s' % (myname, self.awards)
        return myname

    def fullimgname(self):
        if self.source_file_name:
            myname = self.source_file_name
        else:
            myname = self.pid.pid
        if self.variation:
            myname = '%s %s ' % (myname, self.variation)
        if self.form:
            myname = '%s %s form ' % (myname, self.form)
        if self.certainty:
            myname = '%s %s ' % (myname, self.certainty)
        if self.name:
            myname = "%s '%s' " % (myname, self.name)
        if self.awards:
            myname = '%s %s' % (myname, self.awards)

        return myname

    def image_dir(self):
        # return 'utils/images/hybrid/' + block_id + '/'
        return 'utils/images/hybrid/'

    def thumb_dir(self):
        return 'utils/images/hybrid_thumb/'

    def get_displayname(self):
        if self.credit_to:
            return self.credit_to
        return self.author.displayname

    def get_userid(self):
        author = Photographer.objects.get(author=self.author_id)
        return author.user_id

    # def save(self, *args, **kwargs):
    #     if self.image_file_path:
    #         pilImage = Img.open(BytesIO(self.image_file_path.read()))
    #         for orientation in ExifTags.TAGS.keys():
    #             if ExifTags.TAGS[orientation] == 'Orientation':
    #                 break
    #         exif = dict(pilImage._getexif().items())
    #
    #         if exif[orientation] == 3:
    #             pilImage = pilImage.rotate(180, expand=True)
    #         elif exif[orientation] == 6:
    #             pilImage = pilImage.rotate(270, expand=True)
    #         elif exif[orientation] == 8:
    #             pilImage = pilImage.rotate(90, expand=True)
    #
    #         output = BytesIO()
    #         pilImage.save(output, format='JPEG', quality=75)
    #         output.seek(0)
    #         self.image_file_path = File(output, self.image_file_path.name)
    #
    #     return super(HybImages, self).save(*args, **kwargs)

# @receiver(post_delete, sender=HybImages)
# def submission_delete(sender, instance, **kwargs):
#     instance.image_file.delete(False)

class HybImgHistory(models.Model):
    pid = models.ForeignKey(Hybrid, db_column='pid', on_delete=models.CASCADE)
    img_id = models.IntegerField(null=True, blank=True)
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
    action = models.CharField(max_length=50,null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s %s %s' % (self.pid, self.user_id, self.created_date, self.modified_date)


class SpcImgHistory(models.Model):
    pid = models.ForeignKey(Accepted, db_column='pid', on_delete=models.CASCADE)
    img_id = models.IntegerField(null=True, blank=True)
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
    action = models.CharField(max_length=50,null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s %s %s' % (self.pid, self.user_id, self.created_date, self.modified_date)


class ReidentifyHistory(models.Model):
    from_id = models.IntegerField(null=True, blank=True)  #old id after reident
    to_id = models.IntegerField(null=True, blank=True)  #new id after reident
    from_pid = models.ForeignKey(Species, db_column='from_pid', related_name='from_pid', on_delete=models.CASCADE)
    to_pid = models.ForeignKey(Species, db_column='to_pid', related_name='to_pid',on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, db_column='user_id', on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s %s %s' % (self.pid, self.user_id, self.created_date, self.modified_date)


class Country(models.Model):
    # class Meta:
    #     unique_together = (("dist_code", "dist_num", "region"),)
    #     ordering = ['country','region']
    dist_code = models.CharField(max_length=3,primary_key=True)
    dist_num  = models.IntegerField(null=True, blank=True)
    country   = models.CharField(max_length=100,null=True, blank=True)
    region    = models.CharField(max_length=100,null=True, blank=True)
    orig_code = models.CharField(max_length=100,null=True, blank=True)
    uncertainty = models.CharField(max_length=10,null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)


class Continent(models.Model):
    id            = models.IntegerField(primary_key=True)
    name            = models.CharField(max_length=100,null=True, blank=True, unique=True)
    note            = models.CharField(max_length=500,null=True, blank=True)
    source          = models.CharField(max_length=10, null=True, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True, null=True)
    modified_date   = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class Region(models.Model):
    id              = models.IntegerField(primary_key=True)
    continent       = models.ForeignKey(Continent,db_column='continent', on_delete=models.DO_NOTHING,null=True, blank=True)
    name            = models.CharField(max_length=100,null=True, blank=True, unique=True)
    note            = models.CharField(max_length=500,null=True, blank=True)
    source          = models.CharField(max_length=10, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SubRegion(models.Model):
    continent       = models.ForeignKey(Continent, default=0,db_column='continent', on_delete=models.DO_NOTHING,null=True, blank=True)
    region          = models.ForeignKey(Region,db_column='region', on_delete=models.DO_NOTHING,null=True, blank=True)
    code            = models.CharField(primary_key=True,max_length=10, unique=True)
    name            = models.CharField(max_length=100,null=True, blank=True, unique=True)
    note            = models.CharField(max_length=500,null=True, blank=True)
    source          = models.CharField(max_length=10, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class LocalRegion(models.Model):
    id            = models.IntegerField(primary_key=True)
    continent       = models.ForeignKey(Continent,null=True, blank=True,db_column='continent', on_delete=models.DO_NOTHING)
    region          = models.ForeignKey(Region,null=True, blank=True,db_column='region', on_delete=models.DO_NOTHING)
    subregion_code  = models.ForeignKey(SubRegion,null=True, blank=True,db_column='subregion_code', on_delete=models.DO_NOTHING)
    continent_name  = models.CharField(max_length=100,null=True )
    region_name     = models.CharField(max_length=100,null=True)
    name            = models.CharField(max_length=100,null=True, unique=True)
    code            = models.CharField(max_length=100,null=True, blank=True)
    note            = models.CharField(max_length=500,null=True, blank=True)
    source          = models.CharField(max_length=10, null=True, blank=True)
    subregion       = models.CharField(max_length=10,null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class GeoLocation(MPTTModel):
    name = models.CharField(max_length=50, unique=True,null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True,related_name='children')

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['name']

    def __str__(self):
        return self.name


class GeoLoc(models.Model):
    geo_id            = models.CharField(max_length=10, unique=True, null=True, blank=True)
    name              = models.CharField(max_length=100,null=True, blank=True, unique=True)
    note            = models.CharField(max_length=500,null=True, blank=True)
    source          = models.CharField(max_length=20, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Distribution(models.Model):
    id              = models.AutoField(primary_key=True, default=10)
    pid          = models.ForeignKey(Species, on_delete=models.CASCADE,db_column='pid',related_name='dist_pid',null=True, blank=True)
    gen          = models.ForeignKey(Genus, on_delete=models.DO_NOTHING,db_column='gen',related_name='dist_gen',null=True, blank=True)
    source       = models.CharField(max_length=10, blank=True)
    continent_id = models.ForeignKey(Continent, db_column='continent_id',null=True, blank=True,on_delete=models.DO_NOTHING)
    region_id    = models.ForeignKey(Region, db_column='region_id',null=True, blank=True,on_delete=models.DO_NOTHING)
    subregion_code = models.ForeignKey(SubRegion, db_column='subregion_code',null=True, blank=True,on_delete=models.DO_NOTHING)
    dist_code = models.CharField(max_length=10, blank=True)
    localregion_code = models.CharField(max_length=10, blank=True)
    localregion_id = models.ForeignKey(LocalRegion, db_column='localregion_id',null=True, blank=True,on_delete=models.DO_NOTHING)
    orig_code = models.CharField(max_length=100,blank=True)
    dist_status = models.CharField(max_length=10,blank=True)
    confidence  = models.CharField(max_length=10,blank=True)
    comment = models.CharField(max_length=500,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("pid", "region_id","subregion_code","localregion_id"),)

    def name(self):
        name = ''
        if self.localregion_id and self.localregion_id.id > 0 and self.localregion_id.code != 'OO':
            name = name + self.localregion_id.name
            if self.subregion_code:
                name = name + ', ' + self.subregion_code.name + ', ' + self.continent_id.name
        elif self.subregion_code:
            name = name + self.subregion_code.name + ', ' + self.continent_id.name
        elif self.region_id:
            name = name + self.region_id.name
        elif self.continent_id:
            name = name + self.continent_id.name
        return name

    def __str__(self):
        return self.name()

    def subname(self):
        return self.subregion_code.name

    def regname(self):
        return self.region_id.name

    def locname(self):
        return self.localregion_id.name

    def conname(self):
        return self.continent_id.name


class TaxUpdate(models.Model):
    id                  = models.AutoField(primary_key=True, default=10)
    pid                 = models.ForeignKey(Species, on_delete=models.CASCADE,db_column='pid',related_name='update_pid',null=True, blank=True)
    source              = models.CharField(max_length=10, blank=True)
    previous_name       = models.CharField(max_length=500, blank=True)
    previous_status     = models.CharField(max_length=500, blank=True)
    previous_dist       = models.CharField(max_length=500, blank=True)
    created_date        = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now=True)


class Donation(models.Model):
    class Sources:
        STRIPE = 'Stripe'
        PAYPAL = 'Paypal'
        CHOICES = (
            (STRIPE, 'Stripe'),
            (PAYPAL, 'Paypal')
        )

    class Statuses:
        ACCEPTED = "Accepted"
        REJECTED = "Rejected"
        CANCELLED = "Cancelled"
        REFUNDED = "Refunded"
        PENDING = "Pending"
        UNVERIFIED = "Unverified"
        CHOICES = [
            (ACCEPTED, "Accepted"),
            (REJECTED, "Rejected"),
            (CANCELLED, "Cancelled"),
            (REFUNDED, "Refunded"),
            (PENDING, "Pending"),
            (UNVERIFIED, "Unverified"),
        ]

    source = models.CharField(max_length=10, choices=Sources.CHOICES, default=Sources.STRIPE)
    source_id = models.CharField(max_length=255, blank=True, null=True)
    donor_display_name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, choices=Statuses.CHOICES, default=Statuses.UNVERIFIED)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    country_code = models.CharField(max_length=2, null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Donation made by {self.donor_display_name} - ${self.amount}"
