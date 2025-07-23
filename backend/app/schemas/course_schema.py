from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate
from app.models.course import Course


class CourseCreateSchema(SQLAlchemyAutoSchema):
    """用於創建課程的 Schema"""

    subject = fields.String(required=True, validate=validate.Length(min=1, max=255))
    teacher_id = fields.Integer(required=True, validate=validate.Range(min=1))
    description = fields.String(missing="", validate=validate.Length(max=1000))
    price = fields.Decimal(required=True, validate=validate.Range(min=0.01))
    location = fields.String(required=True, validate=validate.Length(min=1, max=255))

    class Meta:
        model = Course
        load_instance = True
        fields = ("subject", "teacher_id", "description", "price", "location")


class CourseUpdateSchema(SQLAlchemyAutoSchema):
    """用於更新課程的 Schema"""

    subject = fields.String(validate=validate.Length(min=1, max=255))
    description = fields.String(validate=validate.Length(max=1000))
    price = fields.Decimal(validate=validate.Range(min=0.01))
    location = fields.String(validate=validate.Length(min=1, max=255))

    class Meta:
        model = Course
        load_instance = True
        fields = ("subject", "description", "price", "location")


class CourseResponseSchema(SQLAlchemyAutoSchema):
    """用於回應課程資料的 Schema"""

    teacher_name = fields.Method("get_teacher_name", dump_only=True)
    teacher_email = fields.Method("get_teacher_email", dump_only=True)
    avatar = fields.Method("get_teacher_avatar", dump_only=True)
    price = fields.Decimal(as_string=False)
    review_count = fields.Method("get_review_count", dump_only=True)
    booking_count = fields.Method("get_booking_count", dump_only=True)

    class Meta:
        model = Course
        load_instance = True
        fields = (
            "id",
            "subject",
            "description",
            "price",
            "location",
            "avg_rating",
            "teacher_id",
            "teacher_name",
            "teacher_email",
            "avatar",
            "review_count",
            "booking_count",
            "created_at",
        )

    def get_teacher_name(self, obj):
        """取得老師名稱"""
        return obj.teacher.name if obj.teacher else None

    def get_teacher_email(self, obj):
        """取得老師信箱"""
        return obj.teacher.email if obj.teacher else None

    def get_teacher_avatar(self, obj):
        """取得老師頭像"""
        return obj.teacher.avatar if obj.teacher else None

    def get_review_count(self, obj):
        """取得評論數量"""
        return len(obj.reviews) if hasattr(obj, "reviews") and obj.reviews else 0

    def get_booking_count(self, obj):
        """取得預約數量"""
        return len(obj.bookings) if hasattr(obj, "bookings") and obj.bookings else 0
