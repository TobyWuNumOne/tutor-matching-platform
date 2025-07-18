from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app.models import User, Teacher, Student, Course, Review, Booking


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_relationships = True


class TeacherSchema(SQLAlchemyAutoSchema):
    user = fields.Nested(UserSchema)

    class Meta:
        model = Teacher
        load_instance = True
        include_relationships = True


class StudentSchema(SQLAlchemyAutoSchema):
    user = fields.Nested(UserSchema)

    class Meta:
        model = Student
        load_instance = True
        include_relationships = True


class CourseSchema(SQLAlchemyAutoSchema):
    teacher = fields.Nested(TeacherSchema)

    class Meta:
        model = Course
        load_instance = True
        include_relationships = True


class ReviewSchema(SQLAlchemyAutoSchema):
    course = fields.Nested(CourseSchema)

    class Meta:
        model = Review
        load_instance = True
        include_relationships = True


class BookingSchema(SQLAlchemyAutoSchema):
    course = fields.Nested(CourseSchema)
    student = fields.Nested(StudentSchema)

    class Meta:
        model = Booking
        load_instance = True
        include_relationships = True
