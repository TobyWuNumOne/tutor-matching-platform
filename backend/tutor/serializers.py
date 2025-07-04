from rest_framework import serializers
from tutor.models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'
class BookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = '__all__'
class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        midel = Reviews
        fields = '__all__'