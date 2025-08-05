from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.course import Course


class CourseCreateSchema(Schema):
    """用於創建課程的 Schema - 使用純 Marshmallow Schema"""

    subject = fields.String(required=True, validate=validate.Length(min=1, max=255))
    teacher_id = fields.Integer(required=True, validate=validate.Range(min=1))
    description = fields.String(allow_none=True, validate=validate.Length(max=1000))
    price = fields.Decimal(required=True, validate=validate.Range(min=0.01))
    location = fields.String(required=True, validate=validate.Length(min=1, max=255))


class CourseUpdateSchema(Schema):
    """用於更新課程的 Schema - 使用純 Marshmallow Schema"""

    subject = fields.String(validate=validate.Length(min=1, max=255))
    description = fields.String(allow_none=True, validate=validate.Length(max=1000))
    price = fields.Decimal(validate=validate.Range(min=0.01))
    location = fields.String(validate=validate.Length(min=1, max=255))


class CourseResponseSchema(SQLAlchemyAutoSchema):
    """用於回傳課程資料的 Schema"""

    # 明確定義 teacher_id 欄位
    teacher_id = fields.Integer(dump_only=True)

    # 關聯資料
    teacher_name = fields.Method("get_teacher_name")
    review_count = fields.Method("get_review_count")
    booking_count = fields.Method("get_booking_count")

    def get_teacher_name(self, obj):
        return obj.teacher.name if obj.teacher else None

    def get_review_count(self, obj):
        return len(obj.reviews) if hasattr(obj, "reviews") and obj.reviews else 0

    def get_booking_count(self, obj):
        return len(obj.bookings) if hasattr(obj, "bookings") and obj.bookings else 0

    class Meta:
        model = Course
        load_instance = False  # 確保不會嘗試創建實例
        fields = (
            "id",
            "subject",
            "teacher_id",
            "description",
            "price",
            "location",
            "avg_rating",
            "created_at",
            "updated_at",
            "teacher_name",
            "review_count",
            "booking_count",
        )


# 簡化的基本課程 Schema（用於避免循環引用）
class CourseBasicSchema(SQLAlchemyAutoSchema):
    """基本課程資料 Schema"""

    teacher_name = fields.Method("get_teacher_name")

    def get_teacher_name(self, obj):
        return obj.teacher.name if obj.teacher else None

    class Meta:
        model = Course
        fields = ("id", "subject", "description", "price", "location", "teacher_name")
