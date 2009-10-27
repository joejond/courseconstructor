from django.db import models as md
from markdown import markdown

class Course(md.Model):
    title = md.CharField(max_length=80)
    slug = md.SlugField()
    code = md.CharField(max_length=4, unique=True)
    description = md.TextField(max_length=50000)
    description_html = md.TextField(max_length=50000, blank=True)
    def __unicode__(self):
        return self.title
    
class BaseSection (md.Model):
    title = md.CharField(max_length=80)
    slug = md.SlugField()
    introduction = md.TextField(max_length=50000)
    introduction_html = md.TextField(max_length=50000, blank=True)
    conclusion = md.TextField(max_length=50000)
    conclusion_html = md.TextField(max_length=50000, blank=True)
    code = md.CharField(max_length=4)
    show = md.BooleanField(default=True)
    
    
    class Meta:
        abstract = True
        
    def save(self, force_insert=False, force_update=False):
        fields = [field[:-5] for field in dir (self) if field[-5:]=="_html"]
        for field in fields:
            if getattr(self, field):
                setattr(self, field +"_html", markdown(getattr(self,field)))
        super(BaseSection, self).save(force_insert, force_update)
        
class Section(BaseSection):
    #Relationships
    course = md.ForeignKey(Course)
    abstract = md.TextField(max_length=50000)
    abstract_html = md.TextField(max_length=50000, blank=True)
    
class Subsection(BaseSection):
    #Relationships
    parent = md.ForeignKey(Section)
    body = md.TextField(max_length=50000)
    body_html = md.TextField(max_length=50000, blank=True)

