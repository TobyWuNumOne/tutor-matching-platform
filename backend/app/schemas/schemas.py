from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app.models import User, Teacher, Student, Course, Review, Booking


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ["password"]  # 排除敏感資訊


class TeacherSchema(SQLAlchemyAutoSchema):
    user_id = fields.Integer(dump_only=True)

    class Meta:
        model = Teacher
        load_instance = True
        exclude = ["created_at", "updated_at", "user"]  # 排除 user 關聯


class StudentSchema(SQLAlchemyAutoSchema):
    user = fields.Nested(UserSchema)

    class Meta:
        model = Student
        load_instance = True
        exclude = ["created_at", "user"]  # 排除 user 關聯


class CourseSchema(SQLAlchemyAutoSchema):
    teacher = fields.Nested(
        TeacherSchema, exclude=["courses"], dump_only=True
    )  # 避免循環參考
    teacher_name = fields.Method(
        "get_teacher_name", dump_only=True
    )  # 自定義方法取得 teacher name
    teacher_email = fields.Method("get_teacher_email", dump_only=True)  # 取得老師信箱
    avatar = fields.Method("get_teacher_avatar", dump_only=True)  # 取得老師頭像
    price = fields.Decimal(as_string=False)  # 確保價格以數字形式返回
    review_count = fields.Method("get_review_count", dump_only=True)  # 評論數量
    booking_count = fields.Method("get_booking_count", dump_only=True)  # 預約數量

    class Meta:
        model = Course
        load_instance = True
        include_relationships = True
        exclude = ["updated_at"]

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


class ReviewSchema(SQLAlchemyAutoSchema):
    course = fields.Nested("CourseBasicSchema", dump_only=True)  # 使用基本的課程 schema
    student = fields.Nested(
        "StudentBasicSchema", dump_only=True
    )  # 使用基本的學生 schema
    rating_float = fields.Method("get_rating_float", dump_only=True)  # 浮點數評分

    class Meta:
        model = Review
        load_instance = True
        include_relationships = True
        exclude = ["updated_at"]

    def get_rating_float(self, obj):
        """取得浮點數格式的評分"""
        return obj.rating_float if hasattr(obj, "rating_float") else 0.0


class BookingSchema(SQLAlchemyAutoSchema):
    course = fields.Nested(
        CourseSchema, exclude=["teacher", "reviews", "bookings"], dump_only=True
    )  # 避免過深的嵌套
    student = fields.Nested(
        StudentSchema, exclude=["user", "bookings", "reviews"], dump_only=True
    )  # 避免循環參考
    course_subject = fields.Method("get_course_subject", dump_only=True)  # 課程科目
    course_price = fields.Method("get_course_price", dump_only=True)  # 課程價格
    course_location = fields.Method("get_course_location", dump_only=True)  # 課程地點
    teacher_name = fields.Method("get_teacher_name", dump_only=True)  # 老師姓名
    student_name = fields.Method("get_student_name", dump_only=True)  # 學生姓名
    student_email = fields.Method("get_student_email", dump_only=True)  # 學生信箱
    schedule_datetime = fields.Method(
        "get_schedule_datetime", dump_only=True
    )  # 格式化的時間

    class Meta:
        model = Booking
        load_instance = True
        include_relationships = True
        exclude = ["updated_at"]

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

    def get_schedule_datetime(self, obj):
        """取得格式化的預約時間"""
        return obj.schedule_date if obj.schedule_date else None


# 簡化版的 Schema，用於嵌套時避免過多資料
class CourseBasicSchema(SQLAlchemyAutoSchema):
    teacher_name = fields.Method("get_teacher_name", dump_only=True)
    price = fields.Decimal(as_string=False)

    class Meta:
        model = Course
        load_instance = True
        fields = ("id", "subject", "description", "price", "location", "teacher_name")

    def get_teacher_name(self, obj):
        return obj.teacher.name if obj.teacher else None


class StudentBasicSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True
        fields = ("id", "name", "email")
