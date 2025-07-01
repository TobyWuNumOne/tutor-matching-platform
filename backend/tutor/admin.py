from django.contrib import admin
from tutor.models import *

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'password', 'role', 'created_at', 'updated_at')
    search_fields = ('name','email', 'role')
    
@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher_id', 'subject', 'price_per_hour', 'location', 'description', 'created_at')
    search_fields = ('id', 'teacher_id', 'subject',)
    filter_horizontal = ('students',) 
@admin.register(Bookings)
class BookingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_id', 'course_id', 'schedule_date', 'status', 'created_at')
    search_fields = ('student_id', 'course_id', 'schedule_date', 'status',)
    
@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_id', 'student_id', 'rating', 'comment', 'created_at')
    search_fields = ('course_id','rating',)
    