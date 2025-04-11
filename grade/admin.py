from django.contrib import admin

# Register your models here.
from .models import Grades

@admin.register(Grades)
class GradesAdmin(admin.ModelAdmin):
    list_display = ('student', 'current_grade', 'total_grade', 'date')
    search_fields = ('student__first_name', 'student__last_name', 'current_grade')
    list_filter = ('date',)
    ordering = ('-date',)