from marshmallow import Schema, fields, validate


class StudentSchema(Schema):
    """學生序列化"""

    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    gender = fields.Str(allow_none=True, validate=validate.Length(max=10))
    age = fields.Str(allow_none=True, validate=validate.Length(max=20))
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)

    # 嵌套用戶資訊
    user = fields.Nested("UserSchema", dump_only=True)
    bookings = fields.Nested("BookingSchema", many=True, dump_only=True)
    reviews = fields.Nested("ReviewSchema", many=True, dump_only=True)


class StudentCreateSchema(Schema):
    """學生建立序列化"""

    email = fields.Email(required=True)
    gender = fields.Str(allow_none=True, validate=validate.Length(max=10))
    age = fields.Str(allow_none=True, validate=validate.Length(max=20))
    user_id = fields.Int(required=True)


class StudentUpdateSchema(Schema):
    """學生更新序列化"""

    email = fields.Email()
    gender = fields.Str(allow_none=True, validate=validate.Length(max=10))
    age = fields.Str(allow_none=True, validate=validate.Length(max=20))
