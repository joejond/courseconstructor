from django.db import models as md
from markdown import markdown

class Course(md.Model):
    title = md.CharField(max_length=80)
    slug = md.SlugField(unique=True)
    code = md.CharField(max_length=4, unique=True)
    description = md.TextField(max_length=50000)
    description_html = md.TextField(max_length=50000, blank=True)
    def __unicode__(self):
        return self.title
    def save(self, force_insert=False, force_update=False):
        if self.description:
                self.description_html = markdown(self.description)
        super(Course, self).save(force_insert, force_update)
    def get_absolute_url(self):
        return "/cw/course/{0}.html".format(self.slug)
    
class BaseSection (md.Model):
    title = md.CharField(max_length=80)
    slug = md.SlugField(unique=True)
    introduction = md.TextField(max_length=50000)
    introduction_html = md.TextField(max_length=50000, blank=True)
    conclusion = md.TextField(max_length=50000)
    conclusion_html = md.TextField(max_length=50000, blank=True)
    code = md.CharField(max_length=4)
    show = md.BooleanField(default=True)
    sortorder = md.IntegerField()
    
    
    class Meta:
        abstract = True
        
    def save(self, force_insert=False, force_update=False):
        fields = [field[:-5] for field in dir (self) if field[-5:]=="_html"]
        for field in fields:
            if getattr(self, field):
                setattr(self, field +"_html", markdown(getattr(self,field)))
        super(BaseSection, self).save(force_insert, force_update)
        
    def get_absolute_url(self):
        className = `self.__class__`.split('.')[3].split(' ')[0].split("'")[0].lower()
        return "/cw/{0}/{1}.html".format(className, self.slug)
        
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

