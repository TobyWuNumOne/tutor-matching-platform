from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from tutor.models import *


@admin.register(Users)
class UsersAdmin(UserAdmin):
    # 基於 Django 的 UserAdmin，但添加我們的自訂欄位
    list_display = (
        "username",
        "email", 
        "get_full_name",  # 使用 Django 內建的 get_full_name
        "role",
        "is_active",
        "date_joined",
    )
    
    list_filter = (
        "role",
        "is_active", 
        "date_joined",
    )
    
    search_fields = ("username", "email", "first_name", "last_name")
    
    # 在編輯用戶時顯示的欄位群組 - 包含密碼管理
    fieldsets = UserAdmin.fieldsets + (
        ('自訂欄位', {'fields': ('role', 'created_at', 'updated_at')}),
    )
    
    # 在新增用戶時顯示的欄位 - 包含密碼設定
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('自訂欄位', {'fields': ('role',)}),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    # 自訂方法來顯示密碼狀態
    def password_status(self, obj):
        if obj.password:
            return format_html('<span style="color: green;">密碼已設定</span>')
        return format_html('<span style="color: red;">未設定密碼</span>')
    password_status.short_description = "密碼狀態"


@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "teacher_id",
        "subject",
        "price_per_hour",
        "location",
        "description",
        "created_at",
    )
    search_fields = (
        "id",
        "teacher_id__username",  # 搜尋教師用戶名
        "subject",
    )
    filter_horizontal = ("students",)


@admin.register(Bookings)
class BookingsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student_id",
        "course_id",
        "schedule_date",
        "status",
        "created_at",
    )
    search_fields = (
        "student_id__username",  # 搜尋學生用戶名
        "course_id__subject",    # 搜尋課程主題
        "status",
    )
    list_filter = ("status", "schedule_date")


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("id", "course_id", "student_id", "rating", "comment", "created_at")
    search_fields = (
        "course_id__subject",    # 搜尋課程主題
        "student_id__username",  # 搜尋學生用戶名
        "rating",
    )
    list_filter = ("rating", "created_at")
