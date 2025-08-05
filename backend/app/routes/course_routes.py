from flask import Blueprint, request, jsonify
from flasgger import swag_from
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.course import Course
from app.models.teacher import Teacher
from app.extensions import db
from app.schemas.course_schema import (
    CourseCreateSchema,
    CourseUpdateSchema,
    CourseResponseSchema,
)

course_bp = Blueprint("courses", __name__)

# 不在全局創建 schema 實例，改為在函數內創建


@course_bp.route("/create", methods=["POST"])
@jwt_required()
@swag_from(
    {
        "tags": ["課程管理"],
        "summary": "建立新課程",
        "description": "老師建立新的課程",
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "description": "課程資料",
                "schema": {
                    "type": "object",
                    "properties": {
                        "subject": {
                            "type": "string",
                            "description": "課程科目",
                            "example": "數學",
                        },
                        "teacher_id": {
                            "type": "integer",
                            "description": "老師ID",
                            "example": 1,
                        },
                        "description": {
                            "type": "string",
                            "description": "課程描述",
                            "example": "高中數學課程，包含代數、幾何等內容",
                        },
                        "price": {
                            "type": "number",
                            "description": "課程價格（每小時）",
                            "example": 800.0,
                        },
                        "location": {
                            "type": "string",
                            "description": "上課地點",
                            "example": "台北市信義區",
                        },
                    },
                    "required": ["subject", "teacher_id", "price", "location"],
                },
            }
        ],
        "responses": {
            201: {
                "description": "課程建立成功",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "message": {"type": "string", "example": "課程建立成功"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "subject": {"type": "string", "example": "數學"},
                                "teacher_id": {"type": "integer", "example": 1},
                                "description": {
                                    "type": "string",
                                    "example": "高中數學課程",
                                },
                                "price": {"type": "number", "example": 800.0},
                                "location": {
                                    "type": "string",
                                    "example": "台北市信義區",
                                },
                                "teacher_name": {"type": "string", "example": "張老師"},
                                "created_at": {
                                    "type": "string",
                                    "example": "2024-07-24T10:00:00",
                                },
                            },
                        },
                    },
                },
            },
            400: {
                "description": "請求參數錯誤",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "message": {"type": "string", "example": "資料驗證失敗"},
                        "errors": {
                            "type": "object",
                            "example": {
                                "subject": ["課程科目不能為空"],
                                "price": ["價格必須大於0"],
                            },
                        },
                    },
                },
            },
            404: {
                "description": "老師不存在",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "message": {"type": "string", "example": "指定的老師不存在"},
                    },
                },
            },
        },
    }
)
def create_course():
    """
    建立新課程
    """
    try:
        # 使用 schema 驗證資料
        try:
            course_create_schema = CourseCreateSchema()
            validated_data = course_create_schema.load(request.json)
        except ValidationError as err:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "資料驗證失敗",
                        "errors": err.messages,
                    }
                ),
                400,
            )

        # 檢查老師是否存在
        teacher = Teacher.query.get(validated_data['teacher_id'])
        if not teacher:
            return jsonify({"success": False, "message": "指定的老師不存在"}), 404

        # 建立新課程
        new_course = Course(
            subject=validated_data['subject'],
            teacher_id=validated_data['teacher_id'],
            description=validated_data.get('description'),
            price=validated_data['price'],
            location=validated_data['location'],
        )

        # 儲存到資料庫
        db.session.add(new_course)
        db.session.commit()

        # 重新查詢以獲取關聯資料
        course_with_relations = Course.query.options(db.joinedload(Course.teacher)).get(
            new_course.id
        )

        # 使用 schema 序列化回應
        course_response_schema = CourseResponseSchema()
        response_data = course_response_schema.dump(course_with_relations)

        return (
            jsonify(
                {"success": True, "message": "課程建立成功", "data": response_data}
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"課程建立失敗: {str(e)}"}), 500


@course_bp.route("/list", methods=["GET"])
@swag_from(
    {
        "tags": ["課程管理"],
        "summary": "獲取課程列表",
        "description": "獲取所有課程的列表，支援篩選和分頁",
        "parameters": [
            {
                "name": "subject",
                "in": "query",
                "type": "string",
                "required": False,
                "description": "科目篩選",
                "example": "數學",
            },
            {
                "name": "teacher_id",
                "in": "query",
                "type": "integer",
                "required": False,
                "description": "老師ID篩選",
                "example": 1,
            },
            {
                "name": "location",
                "in": "query",
                "type": "string",
                "required": False,
                "description": "地點篩選",
                "example": "台北",
            },
            {
                "name": "min_price",
                "in": "query",
                "type": "number",
                "required": False,
                "description": "最低價格",
                "example": 500,
            },
            {
                "name": "max_price",
                "in": "query",
                "type": "number",
                "required": False,
                "description": "最高價格",
                "example": 1000,
            },
            {
                "name": "page",
                "in": "query",
                "type": "integer",
                "required": False,
                "description": "頁碼",
                "example": 1,
            },
            {
                "name": "per_page",
                "in": "query",
                "type": "integer",
                "required": False,
                "description": "每頁筆數",
                "example": 10,
            },
        ],
        "responses": {
            200: {
                "description": "成功獲取課程列表",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "example": 1},
                                    "subject": {"type": "string", "example": "數學"},
                                    "teacher_name": {
                                        "type": "string",
                                        "example": "張老師",
                                    },
                                    "price": {"type": "number", "example": 800.0},
                                    "location": {"type": "string", "example": "台北市"},
                                    "avg_rating": {"type": "number", "example": 4.5},
                                },
                            },
                        },
                        "pagination": {
                            "type": "object",
                            "properties": {
                                "page": {"type": "integer", "example": 1},
                                "per_page": {"type": "integer", "example": 10},
                                "total": {"type": "integer", "example": 50},
                                "pages": {"type": "integer", "example": 5},
                            },
                        },
                    },
                },
            }
        },
    }
)
def get_course_list():
    """
    獲取課程列表
    """
    try:
        # 獲取查詢參數
        subject = request.args.get("subject", "")
        teacher_id = request.args.get("teacher_id", type=int)
        location = request.args.get("location", "")
        min_price = request.args.get("min_price", type=float)
        max_price = request.args.get("max_price", type=float)
        page = request.args.get("page", 1, type=int)
        per_page = min(request.args.get("per_page", 10, type=int), 100)

        # 建立查詢
        query = Course.query.options(db.joinedload(Course.teacher))

        # 套用篩選條件
        if subject:
            query = query.filter(Course.subject.ilike(f"%{subject}%"))

        if teacher_id:
            query = query.filter(Course.teacher_id == teacher_id)

        if location:
            query = query.filter(Course.location.ilike(f"%{location}%"))

        if min_price is not None:
            query = query.filter(Course.price >= min_price)

        if max_price is not None:
            query = query.filter(Course.price <= max_price)

        # 按建立時間降序排列
        query = query.order_by(Course.created_at.desc())

        # 分頁查詢
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        courses = pagination.items

        # 使用 schema 序列化資料
        courses_data = course_response_schema_many.dump(courses)

        return (
            jsonify(
                {
                    "success": True,
                    "data": courses_data,
                    "pagination": {
                        "page": pagination.page,
                        "per_page": pagination.per_page,
                        "total": pagination.total,
                        "pages": pagination.pages,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify({"success": False, "message": f"獲取課程列表失敗: {str(e)}"}),
            500,
        )


@course_bp.route("/<int:course_id>", methods=["GET"])
@swag_from(
    {
        "tags": ["課程管理"],
        "summary": "獲取課程詳細資訊",
        "description": "根據課程ID獲取詳細資訊，包含評論和預約統計",
        "parameters": [
            {
                "name": "course_id",
                "in": "path",
                "type": "integer",
                "required": True,
                "description": "課程ID",
                "example": 1,
            }
        ],
        "responses": {
            200: {
                "description": "成功獲取課程詳細資訊",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "subject": {"type": "string", "example": "數學"},
                                "teacher_name": {"type": "string", "example": "張老師"},
                                "description": {
                                    "type": "string",
                                    "example": "高中數學課程",
                                },
                                "price": {"type": "number", "example": 800.0},
                                "location": {"type": "string", "example": "台北市"},
                                "avg_rating": {"type": "number", "example": 4.5},
                                "review_count": {"type": "integer", "example": 10},
                                "booking_count": {"type": "integer", "example": 25},
                            },
                        },
                    },
                },
            },
            404: {
                "description": "課程不存在",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "message": {"type": "string", "example": "找不到指定的課程"},
                    },
                },
            },
        },
    }
)
def get_course_detail(course_id):
    """
    獲取課程詳細資訊
    """
    try:
        # 查詢課程資訊，包含關聯資料
        course = Course.query.options(
            db.joinedload(Course.teacher),
            db.joinedload(Course.reviews),
            db.joinedload(Course.bookings),
        ).get(course_id)

        if not course:
            return jsonify({"success": False, "message": "找不到指定的課程"}), 404

        # 使用 schema 序列化資料
        course_data = course_response_schema.dump(course)

        return jsonify({"success": True, "data": course_data}), 200

    except Exception as e:
        return (
            jsonify({"success": False, "message": f"獲取課程詳細資訊失敗: {str(e)}"}),
            500,
        )


@course_bp.route("/<int:course_id>", methods=["PUT"])
@swag_from(
    {
        "tags": ["課程管理"],
        "summary": "更新課程資訊",
        "description": "老師更新課程資訊",
        "parameters": [
            {
                "name": "course_id",
                "in": "path",
                "type": "integer",
                "required": True,
                "description": "課程ID",
                "example": 1,
            },
            {
                "name": "body",
                "in": "body",
                "required": True,
                "description": "要更新的課程資料",
                "schema": {
                    "type": "object",
                    "properties": {
                        "subject": {
                            "type": "string",
                            "description": "課程科目",
                            "example": "數學",
                        },
                        "description": {
                            "type": "string",
                            "description": "課程描述",
                            "example": "高中數學課程，包含代數、幾何等內容",
                        },
                        "price": {
                            "type": "number",
                            "description": "課程價格（每小時）",
                            "example": 900.0,
                        },
                        "location": {
                            "type": "string",
                            "description": "上課地點",
                            "example": "台北市信義區",
                        },
                    },
                },
            },
        ],
        "responses": {
            200: {
                "description": "課程更新成功",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "message": {"type": "string", "example": "課程更新成功"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "subject": {"type": "string", "example": "數學"},
                                "description": {
                                    "type": "string",
                                    "example": "高中數學課程",
                                },
                                "price": {"type": "number", "example": 900.0},
                                "location": {
                                    "type": "string",
                                    "example": "台北市信義區",
                                },
                            },
                        },
                    },
                },
            },
            400: {
                "description": "請求參數錯誤",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "message": {"type": "string", "example": "資料驗證失敗"},
                        "errors": {"type": "object"},
                    },
                },
            },
            404: {
                "description": "課程不存在",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "message": {"type": "string", "example": "找不到指定的課程"},
                    },
                },
            },
        },
    }
)
def update_course(course_id):
    """
    更新課程資訊
    """
    try:
        # 查詢課程
        course = Course.query.get(course_id)
        if not course:
            return jsonify({"success": False, "message": "找不到指定的課程"}), 404

        # 使用 schema 驗證資料
        try:
            validated_data = course_update_schema.load(request.json, partial=True)
        except ValidationError as err:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "資料驗證失敗",
                        "errors": err.messages,
                    }
                ),
                400,
            )

        # 更新課程資料
        for key, value in validated_data.items():
            if hasattr(course, key):
                setattr(course, key, value)

        db.session.commit()

        # 重新查詢以獲取關聯資料
        updated_course = Course.query.options(
            db.joinedload(Course.teacher),
            db.joinedload(Course.reviews),
            db.joinedload(Course.bookings),
        ).get(course_id)

        # 使用 schema 序列化回應
        response_data = course_response_schema.dump(updated_course)

        return (
            jsonify(
                {"success": True, "message": "課程更新成功", "data": response_data}
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"課程更新失敗: {str(e)}"}), 500
