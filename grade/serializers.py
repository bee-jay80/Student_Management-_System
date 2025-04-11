from rest_framework import serializers
from .models import Grades


class GradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grades
        fields = ['id', 'current_grade', 'total_grade', 'date', 'student']
        read_only_fields = ['total_grade', 'date']