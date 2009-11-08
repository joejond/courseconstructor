from course_manager import models as cmm
from django.contrib import admin

class SubsectionInline(admin.StackedInline):
    fields = ['title', 'slug', 'code', 'show', 'introduction', 'body', 'conclusion']
    prepopulated_fields = {"slug": ("title",)}
    model = cmm.Subsection
    extra = 2

class SectionInline(admin.TabularInline):
    fields = ['title', 'slug', 'code', 'show', 'sortorder']
    prepopulated_fields = {"slug": ("title",)}
    model = cmm.Section
    extra = 4

class SectionAdmin(admin.ModelAdmin):
    fields = ['course', 'title', 'slug', 'introduction', 'conclusion', 'code', 'show']
    list_display = ['course', 'title', 'code', 'show']
    list_editable = ['show', 'code']
    list_filter = ['course']
    search_fields = ['course__title']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [SubsectionInline]

class CourseAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'code', 'description']
    list_display = ['title', 'code']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [SectionInline]


admin.site.register(cmm.Section, SectionAdmin)
admin.site.register(cmm.Course, CourseAdmin)
