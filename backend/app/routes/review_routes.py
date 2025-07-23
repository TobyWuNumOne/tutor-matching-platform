from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.models.review import Review
from app.models.course import Course
from app.models.booking import Booking
from app.schemas.review_schema import (
    ReviewSchema,
    ReviewCreateSchema,
    ReviewUpdateSchema,
)
from app.extensions import db
from app.utils.auth_required import auth_required
from marshmallow import ValidationError

# 創建 schema 實例
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)
review_create_schema = ReviewCreateSchema()
review_update_schema = ReviewUpdateSchema()


review_bp = Blueprint("reviews", __name__)


@review_bp.route("/create", methods=["POST"])
@auth_required
@swag_from(
    {
        "tags": ["評論管理"],
        "summary": "創建課程評論",
        "description": "學生對已完成的課程創建評論和評分",
        "parameters": [
            {
                "name": "Authorization",
                "in": "header",
                "type": "string",
                "required": True,
                "description": "Bearer token",
                "example": "Bearer your_jwt_token_here",
            },
            {
                "name": "body",
                "in": "body",
                "required": True,
                "description": "評論資訊",
                "schema": {
                    "type": "object",
                    "properties": {
                        "course_id": {
                            "type": "integer",
                            "description": "課程ID",
                            "example": 1,
                        },
                        "rating": {
                            "type": "string",
                            "description": "評分（1-5，可包含小數）",
                            "example": "4.5",
                        },
                        "comment": {
                            "type": "string",
                            "description": "評論內容（可選）",
                            "example": "老師教學很認真，講解清楚",
                        },
                    },
                    "required": ["course_id", "rating"],
                },
            },
        ],
        "responses": {
            201: {
                "description": "評論創建成功",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "message": {"type": "string", "example": "評論創建成功"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "course_id": {"type": "integer", "example": 1},
                                "rating": {"type": "string", "example": "4.5"},
                                "rating_float": {"type": "number", "example": 4.5},
                                "comment": {
                                    "type": "string",
                                    "example": "老師教學很認真",
                                },
                                "course": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer", "example": 1},
                                        "subject": {
                                            "type": "string",
                                            "example": "數學",
                                        },
                                        "teacher_name": {
                                            "type": "string",
                                            "example": "張老師",
                                        },
                                    },
                                },
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
                        "message": {"type": "string", "example": "數據驗證失敗"},
                        "errors": {
                            "type": "object",
                            "example": {"rating": ["評分必須是 1-5 之間的數字"]},
                        },
                    },
                },
            },
            403: {
                "description": "沒有權限",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "message": {
                            "type": "string",
                            "example": "只有完成課程的學生才能評論",
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
                        "message": {"type": "string", "example": "指定的課程不存在"},
                    },
                },
            },
            409: {
                "description": "重複評論",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "message": {
                            "type": "string",
                            "example": "您已經對此課程進行過評論",
                        },
                    },
                },
            },
        },
    }
)
def create_review(current_user):
    """
    創建課程評論
    """
    try:
        # 獲取請求數據
        data = request.get_json()

        # 數據驗證
        try:
            validated_data = review_create_schema.load(data)
        except ValidationError as err:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "數據驗證失敗",
                        "errors": err.messages,
                    }
                ),
                400,
            )

        # 檢查課程是否存在
        course = Course.query.get(validated_data["course_id"])
        if not course:
            return jsonify({"success": False, "message": "指定的課程不存在"}), 404

        # 檢查用戶是否有權限評論（必須是學生且完成了該課程的預約）
        completed_booking = Booking.query.filter_by(
            course_id=validated_data["course_id"],
            student_id=(
                current_user.student.id if hasattr(current_user, "student") else None
            ),
            status="completed",
        ).first()

        if not completed_booking:
            return (
                jsonify({"success": False, "message": "只有完成課程的學生才能評論"}),
                403,
            )

        # 檢查是否已經評論過
        existing_review = Review.query.filter_by(
            course_id=validated_data["course_id"], student_id=current_user.student.id
        ).first()

        if existing_review:
            return (
                jsonify({"success": False, "message": "您已經對此課程進行過評論"}),
                409,
            )

        # 創建新評論
        new_review = Review(
            course_id=validated_data["course_id"],
            student_id=current_user.student.id,
            rating=validated_data["rating"],
            comment=validated_data.get("comment", ""),
        )

        # 保存到數據庫
        db.session.add(new_review)
        db.session.commit()

        # 重新查詢以獲取關聯數據
        review_with_relations = Review.query.options(
            db.joinedload(Review.course).joinedload(Course.teacher)
        ).get(new_review.id)

        # 返回創建的評論
        return (
            jsonify(
                {
                    "success": True,
                    "message": "評論創建成功",
                    "data": review_with_relations.to_dict_with_relations(),
                }
            ),
            201,
        )

    except Exception as e:
        # 如果發生錯誤，回滾事務
        db.session.rollback()
        return jsonify({"success": False, "message": f"評論創建失敗: {str(e)}"}), 500


@review_bp.route("/course/<int:course_id>", methods=["GET"])
@swag_from(
    {
        "tags": ["評論管理"],
        "summary": "獲取課程評論列表",
        "description": "獲取指定課程的所有評論",
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
                "description": "成功獲取課程評論列表",
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
                                    "rating": {"type": "string", "example": "4.5"},
                                    "rating_float": {"type": "number", "example": 4.5},
                                    "comment": {
                                        "type": "string",
                                        "example": "老師教學很認真",
                                    },
                                    "created_at": {
                                        "type": "string",
                                        "example": "2024-07-24T10:00:00",
                                    },
                                },
                            },
                        },
                        "pagination": {
                            "type": "object",
                            "properties": {
                                "page": {"type": "integer", "example": 1},
                                "per_page": {"type": "integer", "example": 10},
                                "total": {"type": "integer", "example": 25},
                                "pages": {"type": "integer", "example": 3},
                            },
                        },
                        "statistics": {
                            "type": "object",
                            "properties": {
                                "average_rating": {"type": "number", "example": 4.2},
                                "total_reviews": {"type": "integer", "example": 25},
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
                        "message": {"type": "string", "example": "指定的課程不存在"},
                    },
                },
            },
        },
    }
)
def get_course_reviews(course_id):
    """
    獲取課程評論列表
    """
    try:
        # 檢查課程是否存在
        course = Course.query.get(course_id)
        if not course:
            return jsonify({"success": False, "message": "指定的課程不存在"}), 404

        # 獲取查詢參數
        page = request.args.get("page", 1, type=int)
        per_page = min(request.args.get("per_page", 10, type=int), 100)

        # 查詢評論
        pagination = (
            Review.query.filter_by(course_id=course_id)
            .order_by(Review.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

        # 序列化評論數據
        reviews_data = reviews_schema.dump(pagination.items)

        # 計算統計數據
        all_reviews = Review.query.filter_by(course_id=course_id).all()
        total_reviews = len(all_reviews)
        average_rating = 0

        if total_reviews > 0:
            total_rating = sum(review.rating_float for review in all_reviews)
            average_rating = round(total_rating / total_reviews, 1)

        return (
            jsonify(
                {
                    "success": True,
                    "data": reviews_data,
                    "pagination": {
                        "page": page,
                        "per_page": per_page,
                        "total": pagination.total,
                        "pages": pagination.pages,
                    },
                    "statistics": {
                        "average_rating": average_rating,
                        "total_reviews": total_reviews,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify({"success": False, "message": f"獲取評論列表失敗: {str(e)}"}),
            500,
        )


@review_bp.route("/<int:review_id>", methods=["GET"])
@swag_from(
    {
        "tags": ["評論管理"],
        "summary": "獲取評論詳情",
        "description": "獲取指定評論的詳細信息",
        "parameters": [
            {
                "name": "review_id",
                "in": "path",
                "type": "integer",
                "required": True,
                "description": "評論ID",
                "example": 1,
            }
        ],
        "responses": {
            200: {
                "description": "成功獲取評論詳情",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "rating": {"type": "string", "example": "4.5"},
                                "rating_float": {"type": "number", "example": 4.5},
                                "comment": {
                                    "type": "string",
                                    "example": "老師教學很認真",
                                },
                                "course": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer", "example": 1},
                                        "subject": {
                                            "type": "string",
                                            "example": "數學",
                                        },
                                        "teacher_name": {
                                            "type": "string",
                                            "example": "張老師",
                                        },
                                    },
                                },
                                "created_at": {
                                    "type": "string",
                                    "example": "2024-07-24T10:00:00",
                                },
                            },
                        },
                    },
                },
            },
            404: {
                "description": "評論不存在",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "message": {"type": "string", "example": "指定的評論不存在"},
                    },
                },
            },
        },
    }
)
def get_review(review_id):
    """
    獲取評論詳情
    """
    try:
        # 查詢評論（包含關聯數據）
        review = Review.query.options(
            db.joinedload(Review.course).joinedload(Course.teacher)
        ).get(review_id)

        if not review:
            return jsonify({"success": False, "message": "指定的評論不存在"}), 404

        # 序列化數據
        review_data = review_schema.dump(review)

        return jsonify({"success": True, "data": review_data}), 200

    except Exception as e:
        return (
            jsonify({"success": False, "message": f"獲取評論詳情失敗: {str(e)}"}),
            500,
        )


@review_bp.route("/<int:review_id>", methods=["PUT"])
@auth_required
@swag_from(
    {
        "tags": ["評論管理"],
        "summary": "更新評論",
        "description": "更新指定評論的內容",
        "parameters": [
            {
                "name": "Authorization",
                "in": "header",
                "type": "string",
                "required": True,
                "description": "Bearer token",
                "example": "Bearer your_jwt_token_here",
            },
            {
                "name": "review_id",
                "in": "path",
                "type": "integer",
                "required": True,
                "description": "評論ID",
                "example": 1,
            },
            {
                "name": "body",
                "in": "body",
                "required": True,
                "description": "更新的評論資訊",
                "schema": {
                    "type": "object",
                    "properties": {
                        "rating": {
                            "type": "string",
                            "description": "評分（1-5，可包含小數）",
                            "example": "5.0",
                        },
                        "comment": {
                            "type": "string",
                            "description": "評論內容",
                            "example": "更新後的評論內容",
                        },
                    },
                },
            },
        ],
        "responses": {
            200: {
                "description": "評論更新成功",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "message": {"type": "string", "example": "評論更新成功"},
                        "data": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 1},
                                "rating": {"type": "string", "example": "5.0"},
                                "comment": {
                                    "type": "string",
                                    "example": "更新後的評論內容",
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
                        "message": {"type": "string", "example": "數據驗證失敗"},
                    },
                },
            },
            403: {
                "description": "沒有權限",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "message": {
                            "type": "string",
                            "example": "您只能更新自己的評論",
                        },
                    },
                },
            },
            404: {
                "description": "評論不存在",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "message": {"type": "string", "example": "指定的評論不存在"},
                    },
                },
            },
        },
    }
)
def update_review(current_user, review_id):
    """
    更新評論
    """
    try:
        # 查詢評論
        review = Review.query.get(review_id)
        if not review:
            return jsonify({"success": False, "message": "指定的評論不存在"}), 404

        # 檢查權限（只能更新自己的評論）
        if review.student_id != current_user.student.id:
            return jsonify({"success": False, "message": "您只能更新自己的評論"}), 403

        # 獲取請求數據
        data = request.get_json()

        # 數據驗證
        try:
            validated_data = review_update_schema.load(data)
        except ValidationError as err:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "數據驗證失敗",
                        "errors": err.messages,
                    }
                ),
                400,
            )

        # 更新評論
        if "rating" in validated_data:
            review.rating = validated_data["rating"]
        if "comment" in validated_data:
            review.comment = validated_data["comment"]

        # 保存更改
        db.session.commit()

        # 重新查詢以獲取關聯數據
        updated_review = Review.query.options(
            db.joinedload(Review.course).joinedload(Course.teacher)
        ).get(review_id)

        return (
            jsonify(
                {
                    "success": True,
                    "message": "評論更新成功",
                    "data": updated_review.to_dict_with_relations(),
                }
            ),
            200,
        )

    except Exception as e:
        # 如果發生錯誤，回滾事務
        db.session.rollback()
        return jsonify({"success": False, "message": f"評論更新失敗: {str(e)}"}), 500


@review_bp.route("/<int:review_id>", methods=["DELETE"])
@auth_required
@swag_from(
    {
        "tags": ["評論管理"],
        "summary": "刪除評論",
        "description": "刪除指定的評論",
        "parameters": [
            {
                "name": "Authorization",
                "in": "header",
                "type": "string",
                "required": True,
                "description": "Bearer token",
                "example": "Bearer your_jwt_token_here",
            },
            {
                "name": "review_id",
                "in": "path",
                "type": "integer",
                "required": True,
                "description": "評論ID",
                "example": 1,
            },
        ],
        "responses": {
            200: {
                "description": "評論刪除成功",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": True},
                        "message": {"type": "string", "example": "評論刪除成功"},
                    },
                },
            },
            403: {
                "description": "沒有權限",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "message": {
                            "type": "string",
                            "example": "您只能刪除自己的評論",
                        },
                    },
                },
            },
            404: {
                "description": "評論不存在",
                "schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "message": {"type": "string", "example": "指定的評論不存在"},
                    },
                },
            },
        },
    }
)
def delete_review(current_user, review_id):
    """
    刪除評論
    """
    try:
        # 查詢評論
        review = Review.query.get(review_id)
        if not review:
            return jsonify({"success": False, "message": "指定的評論不存在"}), 404

        # 檢查權限（只能刪除自己的評論）
        if review.student_id != current_user.student.id:
            return jsonify({"success": False, "message": "您只能刪除自己的評論"}), 403

        # 刪除評論
        db.session.delete(review)
        db.session.commit()

        return jsonify({"success": True, "message": "評論刪除成功"}), 200

    except Exception as e:
        # 如果發生錯誤，回滾事務
        db.session.rollback()
        return jsonify({"success": False, "message": f"評論刪除失敗: {str(e)}"}), 500
