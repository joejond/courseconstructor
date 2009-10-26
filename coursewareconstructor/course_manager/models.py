from django.db import models as md

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

