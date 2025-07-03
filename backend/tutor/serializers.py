from rest_framework import serializers
from tutor.models import *


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'