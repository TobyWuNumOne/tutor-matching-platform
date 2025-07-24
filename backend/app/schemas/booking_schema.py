from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate
from app.models.booking import Booking


class BookingCreateSchema(SQLAlchemyAutoSchema):
    """用於創建預約的 Schema"""
    
    course_id = fields.Integer(required=True, validate=validate.Range(min=1))
    student_id = fields.Integer(required=True, validate=validate.Range(min=1))
    schedule_date = fields.DateTime(required=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = Booking
        load_instance = True
        fields = ("course_id", "student_id", "schedule_date")


class BookingUpdateSchema(SQLAlchemyAutoSchema):
    """用於更新預約的 Schema"""
    
    status = fields.String(validate=validate.OneOf(['pending', 'confirmed', 'completed', 'cancelled']))

    class Meta:
        model = Booking
        load_instance = True
        fields = ("status",)


class BookingResponseSchema(SQLAlchemyAutoSchema):
    """用於回傳預約資料的 Schema"""
    
    # 明確定義外鍵欄位
    course_id = fields.Integer(dump_only=True)
    student_id = fields.Integer(dump_only=True)
    
    # 關聯資料
    course_name = fields.Method("get_course_name")
    student_name = fields.Method("get_student_name")
    teacher_name = fields.Method("get_teacher_name")
    
    def get_course_name(self, obj):
        return obj.course.subject if obj.course else None
    
    def get_student_name(self, obj):
        return obj.student.user.name if obj.student and obj.student.user else None
    
    def get_teacher_name(self, obj):
        return obj.course.teacher.user.name if obj.course and obj.course.teacher and obj.course.teacher.user else None

    class Meta:
        model = Booking
        fields = (
            "id",
            "course_id",
            "student_id",
            "schedule_date",
            "status",
            "created_at",
            "updated_at",
            "course_name",
            "student_name",
            "teacher_name"
        )


# 簡化版本的預約 Schema（避免循環引用）
class BookingBasicSchema(SQLAlchemyAutoSchema):
    """基本預約資料 Schema"""
    
    course_name = fields.Method("get_course_name")
    student_name = fields.Method("get_student_name")
    
    def get_course_name(self, obj):
        return obj.course.subject if obj.course else None
    
    def get_student_name(self, obj):
        return obj.student.user.name if obj.student and obj.student.user else None
    
    class Meta:
        model = Booking
        fields = ("id", "schedule_date", "status", "course_name", "student_name")