from marshmallow import Schema, fields, validate


class TeacherSchema(Schema):
    """教師序列化"""

    id = fields.Int(dump_only=True)
    avatar = fields.Str(allow_none=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    phone = fields.Str(allow_none=True, validate=validate.Length(max=20))
    gender = fields.Str(allow_none=True, validate=validate.Length(max=10))
    age = fields.Str(allow_none=True, validate=validate.Length(max=20))
    education = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    certifications = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    intro = fields.Str(required=True)
    teaching_experience = fields.Str(required=True)
    status = fields.Str(allow_none=True, validate=validate.Length(max=20))
    blue_premium = fields.Bool(load_default=False)
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)

    # 嵌套用戶資訊
    user = fields.Nested("UserSchema", dump_only=True)
    courses = fields.Nested("CourseSchema", many=True, dump_only=True)


class TeacherCreateSchema(Schema):
    """教師建立序列化"""

    avatar = fields.Str(allow_none=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    phone = fields.Str(allow_none=True, validate=validate.Length(max=20))
    gender = fields.Str(allow_none=True, validate=validate.Length(max=10))
    age = fields.Str(allow_none=True, validate=validate.Length(max=20))
    education = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    certifications = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    intro = fields.Str(required=True)
    teaching_experience = fields.Str(required=True)
    status = fields.Str(allow_none=True, validate=validate.Length(max=20))
    blue_premium = fields.Bool(load_default=False)
    user_id = fields.Int(required=True)


class TeacherUpdateSchema(Schema):
    """教師更新序列化"""

    avatar = fields.Str(allow_none=True)
    name = fields.Str(validate=validate.Length(min=1, max=100))
    email = fields.Email()
    phone = fields.Str(allow_none=True, validate=validate.Length(max=20))
    gender = fields.Str(allow_none=True, validate=validate.Length(max=10))
    age = fields.Str(allow_none=True, validate=validate.Length(max=20))
    education = fields.Str(validate=validate.Length(min=1, max=100))
    certifications = fields.Str(validate=validate.Length(min=1, max=255))
    intro = fields.Str()
    teaching_experience = fields.Str()
    status = fields.Str(allow_none=True, validate=validate.Length(max=20))
    blue_premium = fields.Bool()
