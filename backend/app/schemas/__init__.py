from .user_schema import (
    UserSchema,
    UserCreateSchema,
    UserUpdateSchema,
    UserResponseSchema,
)
from .teacher_schema import TeacherSchema, TeacherCreateSchema, TeacherUpdateSchema
from .student_schema import StudentSchema, StudentCreateSchema, StudentUpdateSchema

__all__ = [
    "UserSchema",
    "UserCreateSchema",
    "UserUpdateSchema",
    "UserResponseSchema",
    "TeacherSchema",
    "TeacherCreateSchema",
    "TeacherUpdateSchema",
    "StudentSchema",
    "StudentCreateSchema",
    "StudentUpdateSchema",
]
