from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app.models import User, Teacher, Student, Course#, Review, Booking


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ['password']  # 排除敏感資訊


class TeacherSchema(SQLAlchemyAutoSchema):
    user_id = fields.Integer(dump_only=True)

    class Meta:
        model = Teacher
        load_instance = True
        exclude = ['created_at', 'updated_at', 'user']  # 排除 user 關聯


class StudentSchema(SQLAlchemyAutoSchema):
    user = fields.Nested(UserSchema)

    class Meta:
        model = Student
        load_instance = True
        exclude = ['created_at', 'user']  # 排除 user 關聯



class CourseSchema(SQLAlchemyAutoSchema):
    teacher = fields.Nested(TeacherSchema, exclude=['courses'])  # 避免循環參考
    teacher_name = fields.Method("get_teacher_name")  # 自定義方法取得 teacher name

    class Meta:
        model = Course
        load_instance = True
        include_relationships = True
        exclude = ['created_at']
    def get_teacher_name(self, obj):
        """取得老師名稱"""
        return obj.teacher.name if obj.teacher else None

# class ReviewSchema(SQLAlchemyAutoSchema):
#     course = fields.Nested(CourseSchema)

#     class Meta:
#         model = Review
#         load_instance = True
#         include_relationships = True


# class BookingSchema(SQLAlchemyAutoSchema):
#     course = fields.Nested(CourseSchema)
#     student = fields.Nested(StudentSchema)

#     class Meta:
#         model = Booking
#         load_instance = True
#         include_relationships = True
