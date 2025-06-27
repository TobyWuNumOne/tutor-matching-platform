from django.contrib import admin
from tutor.models import *

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'phone')
    search_fields = ('name',)
    filter_horizontal = ('student',)
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search_fields = ('name',) 