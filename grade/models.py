from django.db import models
from django.utils.translation import gettext_lazy as _


from students.models import Student
# Create your models here.
class Grades(models.Model):
    id = models.AutoField(primary_key=True)
    current_grade = models.IntegerField(verbose_name=_("Current Grade"))
    total_grade = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')

    # update total_grade based on previous total_grade + current_grade
    def save(self, *args, **kwargs):
        if self.pk is None:
            previous_grade = Grades.objects.filter(student=self.student).order_by('-created_at').first()
            if previous_grade:
                self.total_grade = previous_grade.total_grade + self.current_grade
            else:
                self.total_grade = self.current_grade
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.current_grade}"