from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate, ValidationError
from app.models.review import Review
from app.models.course import Course


class ReviewSchema(SQLAlchemyAutoSchema):
    """評論序列化器"""

    # 自定義驗證字段
    rating = fields.String(
        required=True,
        validate=validate.Regexp(
            r"^([1-5](\.[0-9])?)$", error="評分必須是 1-5 之間的數字，可以包含小數點"
        ),
    )
    comment = fields.String(
        validate=validate.Length(max=1000, error="評論內容不能超過 1000 字符")
    )
    course_id = fields.Integer(required=True)

    # 只輸出不輸入
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    rating_float = fields.Float(dump_only=True)

    # 關聯數據
    course = fields.Nested("CourseBasicSchema", dump_only=True)

    class Meta:
        model = Review
        load_instance = True
        include_fk = True


class CourseBasicSchema(SQLAlchemyAutoSchema):
    """課程基本信息序列化器（避免循環引用）"""

    teacher_name = fields.Method("get_teacher_name")

    class Meta:
        model = Course
        load_instance = True
        fields = ("id", "subject", "description", "price", "teacher_name")

    def get_teacher_name(self, obj):
        """獲取老師姓名"""
        return obj.teacher.name if obj.teacher else None


class ReviewCreateSchema(SQLAlchemyAutoSchema):
    """創建評論的序列化器"""

    rating = fields.String(
        required=True,
        validate=validate.Regexp(
            r"^([1-5](\.[0-9])?)$", error="評分必須是 1-5 之間的數字，可以包含小數點"
        ),
    )
    comment = fields.String(
        validate=validate.Length(max=1000, error="評論內容不能超過 1000 字符")
    )
    course_id = fields.Integer(required=True)

    class Meta:
        model = Review
        load_instance = True
        fields = ("course_id", "rating", "comment")


class ReviewUpdateSchema(SQLAlchemyAutoSchema):
    """更新評論的序列化器"""

    rating = fields.String(
        validate=validate.Regexp(
            r"^([1-5](\.[0-9])?)$", error="評分必須是 1-5 之間的數字，可以包含小數點"
        )
    )
    comment = fields.String(
        validate=validate.Length(max=1000, error="評論內容不能超過 1000 字符")
    )

    class Meta:
        model = Review
        load_instance = True
        fields = ("rating", "comment")
