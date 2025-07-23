from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate
from app.models.booking import Booking


class BookingCreateSchema(SQLAlchemyAutoSchema):
    """用於創建預約的 Schema"""

    course_id = fields.Integer(required=True, validate=validate.Range(min=1))
    student_id = fields.Integer(required=True, validate=validate.Range(min=1))
    schedule_date = fields.String(required=True, validate=validate.Length(min=1))
    message = fields.String(missing="", validate=validate.Length(max=500))

    class Meta:
        model = Booking
        load_instance = True
        fields = ("course_id", "student_id", "schedule_date", "message")


class BookingUpdateSchema(SQLAlchemyAutoSchema):
    """用於更新預約狀態的 Schema"""

    status = fields.String(
        required=True,
        validate=validate.OneOf(["pending", "confirmed", "completed", "cancelled"]),
    )
    reason = fields.String(missing="", validate=validate.Length(max=500))

    class Meta:
        model = Booking
        load_instance = True
        fields = ("status", "reason")


class BookingResponseSchema(SQLAlchemyAutoSchema):
    """用於回應預約資料的 Schema"""

    course_subject = fields.Method("get_course_subject", dump_only=True)
    course_price = fields.Method("get_course_price", dump_only=True)
    course_location = fields.Method("get_course_location", dump_only=True)
    teacher_name = fields.Method("get_teacher_name", dump_only=True)
    student_name = fields.Method("get_student_name", dump_only=True)
    student_email = fields.Method("get_student_email", dump_only=True)

    class Meta:
        model = Booking
        load_instance = True
        fields = (
            "id",
            "course_id",
            "student_id",
            "schedule_date",
            "status",
            "course_subject",
            "course_price",
            "course_location",
            "teacher_name",
            "student_name",
            "student_email",
            "created_at",
            "updated_at",
        )

    def get_course_subject(self, obj):
        """取得課程科目"""
        return obj.course.subject if obj.course else None

    def get_course_price(self, obj):
        """取得課程價格"""
        return float(obj.course.price) if obj.course and obj.course.price else None

    def get_course_location(self, obj):
        """取得課程地點"""
        return obj.course.location if obj.course else None

    def get_teacher_name(self, obj):
        """取得老師姓名"""
        return obj.course.teacher.name if obj.course and obj.course.teacher else None

    def get_student_name(self, obj):
        """取得學生姓名"""
        return obj.student.name if obj.student else None

    def get_student_email(self, obj):
        """取得學生信箱"""
        return obj.student.email if obj.student else None
