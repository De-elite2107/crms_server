from django.contrib import admin
from .models import *
from django import forms

admin.site.site_header = "Course Resources Management System"
admin.site.site_title = "Admin Title"
admin.site.index_title = "Welcome to Your CRMS Admin Panel"

class ModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_superuser')  # Columns to display
    list_filter = ('is_active', 'is_superuser', 'is_staff', 'role')
    search_fields = ('username', 'email', 'role')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit queryset for instructor field to only users with admin role
        self.fields['instructor'].queryset = User.objects.filter(role='admin') | User.objects.filter(role='lecturer')

class CourseAdmin(admin.ModelAdmin):
    form = CourseForm
    list_display = ('title', 'status', 'unit', 'instructor')  # Columns to display
    search_fields = ('title', 'status', 'unit', 'instructor')
    list_filter = ('status', 'instructor', 'unit')
# Register your models here.
admin.site.register(User, ModelAdmin)
admin.site.register(Course, CourseAdmin)
class ResourceFileInline(admin.TabularInline):
    model = ResourceFile
    extra = 1  # Number of empty forms to display

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    inlines = [ResourceFileInline]  # Include ResourceFile inline in Resource admin
    list_display = ['course', 'resource_type']
    search_fields = ['course', 'resource_type']
    list_filter = ['resource_type']

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'due_date']
    search_fields = ['title', 'description']
    list_filter = ['course', 'due_date']

@admin.register(AssignmentResponse)
class AssignmentResponseAdmin(admin.ModelAdmin):
    list_display = ['user', 'assignment', 'submission_date', 'response_text']
    search_fields = ['user__username', 'assignment__title']
    list_filter = ['assignment', 'user']
