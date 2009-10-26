from course_manager import models as cmm
from django.contrib import admin

class SubsectionInline(admin.StackedInline):
    fields = ['title', 'code', 'show', 'introduction', 'body', 'conclusion']
    model = cmm.Subsection
    extra = 1

class SectionInline(admin.StackedInline):
    fields = ['title', 'code', 'show']
    model = cmm.Section
    extra = 1

class SectionAdmin(admin.ModelAdmin):
    fields = ['course', 'title', 'introduction', 'conclusion', 'code', 'show']
    extra = 1
    inlines = [SubsectionInline]

class CourseAdmin(admin.ModelAdmin):
    fields = ['title', 'code']
    inlines = [SectionInline]


admin.site.register(cmm.Section, SectionAdmin)
admin.site.register(cmm.Course, CourseAdmin)
