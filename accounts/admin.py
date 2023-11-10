from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import CustomUser, Student_Interest

class InterestInline(admin.TabularInline):
    model = Student_Interest

class CustomUserAdmin(UserAdmin):
    inlines = [
        InterestInline,
    ]
    add_fieldsets = (
        None, {
            'classes': ('wide',),
            'fields': ('student_name','student_id','student_programme','student_level','student_mail','password1', 'password2', 'is_staff', 'is_active'),
        }),


    fieldsets = (
        (None, {'fields': ('student_id', 'password')}),
        ('Personal info', {'fields': ('student_name', 'student_programme', 'student_level', 'student_mail')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    ordering = ('student_id',)
    list_display = ['student_name','student_id','student_programme','student_level','student_mail', ]
    



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student_Interest)