from django.contrib import admin

# Register your models here.

from .models import Student, Courses, ProfileImage

admin.site.register(Student)
admin.site.register(Courses)
admin.site.register(ProfileImage)