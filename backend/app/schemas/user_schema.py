from marshmallow import Schema, fields, validate


class UserResponseSchema(Schema):
    """使用者回應序列化 - 只包含安全的欄位"""

    id = fields.Int()
    name = fields.Str()
    account = fields.Str()
    role = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class UserSchema(Schema):
    """使用者序列化 - 包含所有欄位但排除密碼"""

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    account = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    role = fields.Str(
        required=True, validate=validate.OneOf(["teacher", "student", "admin"])
    )
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        exclude = ("password",)


class UserCreateSchema(Schema):
    """使用者建立序列化"""

    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    account = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=6, max=100))
    role = fields.Str(
        required=True, validate=validate.OneOf(["teacher", "student", "admin"])
    )


class UserUpdateSchema(Schema):
    """使用者更新序列化"""

    name = fields.Str(validate=validate.Length(min=1, max=100))
    account = fields.Str(validate=validate.Length(min=3, max=50))
    password = fields.Str(validate=validate.Length(min=6, max=100))
    role = fields.Str(validate=validate.OneOf(["teacher", "student", "admin"]))
