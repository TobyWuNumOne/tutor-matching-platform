from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=255, null=False)
    subject = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=255, null=True)
    student = models.ManyToManyField(
        to="tutor.Student",
        related_name="teacher",
        null=True
    )
    class Meta:
        db_table = 'teacher'
    
    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'student'