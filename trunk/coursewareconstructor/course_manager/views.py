from django.http import HttpResponse
from django.shortcuts import render_to_response
from course_manager import models as cmm

def index(request):
    courses = cmm.Course.objects.all()
    return render_to_response('cw/index.html', locals())

def home(request):
    return render_to_response('index.html', locals())

def show_course(request, slug):
    course = cmm.Course.objects.get(slug=slug)
    sections = course.section_set.order_by("sortorder")
    return render_to_response('cw/course.html', locals())


def show_section(request, slug):
    section = cmm.Section.objects.get(slug=slug)
    return render_to_response('cw/section.html', locals())
    