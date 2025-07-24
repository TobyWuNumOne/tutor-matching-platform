from flask import Blueprint, request, jsonify
from flasgger import swag_from
from marshmallow import ValidationError
from datetime import datetime
from app.models.booking import Booking
from app.models.course import Course
from app.models.student import Student
from app.schemas.booking_schema import (
    BookingCreateSchema,
    BookingUpdateSchema,
    BookingResponseSchema,
)
from app.extensions import db
from app.utils.auth_required import auth_required

# 創建 schema 實例
booking_create_schema = BookingCreateSchema()
booking_update_schema = BookingUpdateSchema()
booking_response_schema = BookingResponseSchema()
booking_response_schema_many = BookingResponseSchema(many=True)

booking_bp = Blueprint('bookings', __name__)


@booking_bp.route('/create', methods=['POST'])
@swag_from({
    'tags': ['預約管理'],
    'summary': '學生建立預約',
    'description': '學生對特定課程建立預約申請',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': '預約資訊',
            'schema': {
                'type': 'object',
                'properties': {
                    'course_id': {
                        'type': 'integer',
                        'description': '課程ID',
                        'example': 1
                    },
                    'student_id': {
                        'type': 'integer',
                        'description': '學生ID',
                        'example': 1
                    },
                    'schedule_date': {
                        'type': 'string',
                        'description': '預約時間（格式：YYYY-MM-DD HH:MM）',
                        'example': '2024-07-25 14:30'
                    }
                },
                'required': ['course_id', 'student_id', 'schedule_date']
            }
        }
    ],
    'responses': {
        201: {
            'description': '預約建立成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': '預約申請已送出'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'course_id': {'type': 'integer', 'example': 1},
                            'student_id': {'type': 'integer', 'example': 1},
                            'schedule_date': {'type': 'string', 'example': '2024-07-25 14:30'},
                            'status': {'type': 'string', 'example': 'pending'},
                            'created_at': {'type': 'string', 'example': '2024-07-23T10:00:00'}
                        }
                    }
                }
            }
        },
        400: {
            'description': '請求參數錯誤',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '資料驗證失敗'},
                    'errors': {
                        'type': 'object',
                        'example': {
                            'schedule_date': ['預約時間格式錯誤']
                        }
                    }
                }
            }
        },
        404: {
            'description': '課程或學生不存在',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '指定的課程不存在'}
                }
            }
        },
        409: {
            'description': '預約衝突',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '該時段已有其他預約'}
                }
            }
        }
    }
})
def create_booking():
    """
    建立新預約
    """
    try:
        # 使用 schema 驗證資料
        try:
            validated_data = booking_create_schema.load(request.json)
        except ValidationError as err:
            return jsonify({
                'success': False,
                'message': '資料驗證失敗',
                'errors': err.messages
            }), 400
        
        # 檢查課程是否存在
        course = Course.query.get(validated_data['course_id'])
        if not course:
            return jsonify({
                'success': False,
                'message': '指定的課程不存在'
            }), 404
        
        # 檢查學生是否存在
        student = Student.query.get(validated_data['student_id'])
        if not student:
            return jsonify({
                'success': False,
                'message': '指定的學生不存在'
            }), 404
        
        # 檢查是否已有相同時間的預約（避免衝突）
        existing_booking = Booking.query.filter_by(
            course_id=validated_data['course_id'],
            schedule_date=validated_data['schedule_date'],
            status='confirmed'
        ).first()
        
        if existing_booking:
            return jsonify({
                'success': False,
                'message': '該時段已有其他預約'
            }), 409
        
        # 建立新預約
        new_booking = Booking(
            course_id=validated_data['course_id'],
            student_id=validated_data['student_id'],
            schedule_date=validated_data['schedule_date'],
            status='pending'
        )
        
        # 儲存到資料庫
        db.session.add(new_booking)
        db.session.commit()
        
        # 重新查詢以獲取關聯資料
        booking_with_relations = Booking.query.options(
            db.joinedload(Booking.course),
            db.joinedload(Booking.student)
        ).get(new_booking.id)
        
        # 使用 schema 序列化回應
        response_data = booking_response_schema.dump(booking_with_relations)
        
        return jsonify({
            'success': True,
            'message': '預約申請已送出',
            'data': response_data
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'預約建立失敗: {str(e)}'
        }), 500


@booking_bp.route('/list', methods=['GET'])
@swag_from({
    'tags': ['預約管理'],
    'summary': '獲取預約列表',
    'description': '獲取預約列表，支援篩選',
    'parameters': [
        {
            'name': 'status',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': '預約狀態篩選',
            'enum': ['pending', 'confirmed', 'completed', 'cancelled'],
            'example': 'pending'
        },
        {
            'name': 'course_id',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': '課程ID篩選',
            'example': 1
        },
        {
            'name': 'student_id',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': '學生ID篩選',
            'example': 1
        },
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': '頁碼',
            'example': 1
        },
        {
            'name': 'per_page',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': '每頁筆數',
            'example': 10
        }
    ],
    'responses': {
        200: {
            'description': '成功獲取預約列表',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'course_id': {'type': 'integer', 'example': 1},
                                'student_id': {'type': 'integer', 'example': 1},
                                'schedule_date': {'type': 'string', 'example': '2024-07-25 14:30'},
                                'status': {'type': 'string', 'example': 'pending'},
                                'created_at': {'type': 'string', 'example': '2024-07-23T10:00:00'}
                            }
                        }
                    },
                    'pagination': {
                        'type': 'object',
                        'properties': {
                            'page': {'type': 'integer', 'example': 1},
                            'per_page': {'type': 'integer', 'example': 10},
                            'total': {'type': 'integer', 'example': 50},
                            'pages': {'type': 'integer', 'example': 5}
                        }
                    }
                }
            }
        }
    }
})
def get_booking_list():
    """
    獲取預約列表
    """
    try:
        # 獲取查詢參數
        status = request.args.get('status')
        course_id = request.args.get('course_id', type=int)
        student_id = request.args.get('student_id', type=int)
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        # 建立查詢
        query = Booking.query.options(
            db.joinedload(Booking.course),
            db.joinedload(Booking.student)
        )
        
        # 套用篩選條件
        if status:
            query = query.filter(Booking.status == status)
        
        if course_id:
            query = query.filter(Booking.course_id == course_id)
        
        if student_id:
            query = query.filter(Booking.student_id == student_id)
        
        # 按建立時間降序排列
        query = query.order_by(Booking.created_at.desc())
        
        # 分頁查詢
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        bookings = pagination.items
        
        # 使用 schema 序列化資料
        bookings_data = booking_response_schema_many.dump(bookings)
        
        return jsonify({
            'success': True,
            'data': bookings_data,
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'獲取預約列表失敗: {str(e)}'
        }), 500


@booking_bp.route('/<int:booking_id>', methods=['GET'])
@swag_from({
    'tags': ['預約管理'],
    'summary': '獲取預約詳細資訊',
    'description': '根據預約ID獲取詳細資訊',
    'parameters': [
        {
            'name': 'booking_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': '預約ID',
            'example': 1
        }
    ],
    'responses': {
        200: {
            'description': '成功獲取預約詳細資訊',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'course_id': {'type': 'integer', 'example': 1},
                            'student_id': {'type': 'integer', 'example': 1},
                            'schedule_date': {'type': 'string', 'example': '2024-07-25 14:30'},
                            'status': {'type': 'string', 'example': 'pending'},
                            'created_at': {'type': 'string', 'example': '2024-07-23T10:00:00'}
                        }
                    }
                }
            }
        },
        404: {
            'description': '預約不存在',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '找不到指定的預約'}
                }
            }
        }
    }
})
def get_booking_detail(booking_id):
    """
    獲取預約詳細資訊
    """
    try:
        # 查詢預約資訊，包含關聯資料
        booking = Booking.query.options(
            db.joinedload(Booking.course),
            db.joinedload(Booking.student)
        ).get(booking_id)
        
        if not booking:
            return jsonify({
                'success': False,
                'message': '找不到指定的預約'
            }), 404
        
        # 使用 schema 序列化資料
        booking_data = booking_response_schema.dump(booking)
        
        return jsonify({
            'success': True,
            'data': booking_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'獲取預約詳細資訊失敗: {str(e)}'
        }), 500


@booking_bp.route('/<int:booking_id>', methods=['PUT'])
@auth_required
@swag_from({
    'tags': ['預約管理'],
    'summary': '更新預約狀態',
    'description': '老師或學生更新預約狀態',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token',
            'example': 'Bearer your_jwt_token_here'
        },
        {
            'name': 'booking_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': '預約ID',
            'example': 1
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': '要更新的預約資料',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {
                        'type': 'string',
                        'description': '預約狀態',
                        'enum': ['pending', 'confirmed', 'completed', 'cancelled'],
                        'example': 'confirmed'
                    },
                    'reason': {
                        'type': 'string',
                        'description': '狀態變更原因（可選）',
                        'example': '時間衝突'
                    }
                },
                'required': ['status']
            }
        }
    ],
    'responses': {
        200: {
            'description': '預約更新成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': '預約狀態更新成功'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'status': {'type': 'string', 'example': 'confirmed'},
                            'reason': {'type': 'string', 'example': '時間衝突'}
                        }
                    }
                }
            }
        },
        400: {
            'description': '請求參數錯誤',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '資料驗證失敗'},
                    'errors': {'type': 'object'}
                }
            }
        },
        403: {
            'description': '沒有權限',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '您沒有權限修改此預約'}
                }
            }
        },
        404: {
            'description': '預約不存在',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '找不到指定的預約'}
                }
            }
        }
    }
})
def update_booking(current_user, booking_id):
    """
    更新預約狀態
    """
    try:
        # 查詢預約
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({
                'success': False,
                'message': '找不到指定的預約'
            }), 404
        
        # 檢查權限（老師或學生可以更新相關的預約）
        is_teacher = (hasattr(current_user, 'teacher') and 
                     current_user.teacher and 
                     booking.course.teacher_id == current_user.teacher.id)
        is_student = (hasattr(current_user, 'student') and 
                     current_user.student and 
                     booking.student_id == current_user.student.id)
        
        if not (is_teacher or is_student):
            return jsonify({
                'success': False,
                'message': '您沒有權限修改此預約'
            }), 403
        
        # 使用 schema 驗證資料
        try:
            validated_data = booking_update_schema.load(request.json, partial=True)
        except ValidationError as err:
            return jsonify({
                'success': False,
                'message': '資料驗證失敗',
                'errors': err.messages
            }), 400
        
        # 更新預約資料
        for key, value in validated_data.items():
            if hasattr(booking, key):
                setattr(booking, key, value)
        
        db.session.commit()
        
        # 重新查詢以獲取關聯資料
        updated_booking = Booking.query.options(
            db.joinedload(Booking.course),
            db.joinedload(Booking.student)
        ).get(booking_id)
        
        # 使用 schema 序列化回應
        response_data = booking_response_schema.dump(updated_booking)
        
        return jsonify({
            'success': True,
            'message': '預約狀態更新成功',
            'data': response_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'預約更新失敗: {str(e)}'
        }), 500


@booking_bp.route('/<int:booking_id>', methods=['DELETE'])
@auth_required
@swag_from({
    'tags': ['預約管理'],
    'summary': '刪除預約',
    'description': '刪除指定的預約',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token',
            'example': 'Bearer your_jwt_token_here'
        },
        {
            'name': 'booking_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': '預約ID',
            'example': 1
        }
    ],
    'responses': {
        200: {
            'description': '預約刪除成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': '預約刪除成功'}
                }
            }
        },
        403: {
            'description': '沒有權限',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '您沒有權限刪除此預約'}
                }
            }
        },
        404: {
            'description': '預約不存在',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '找不到指定的預約'}
                }
            }
        }
    }
})
def delete_booking(current_user, booking_id):
    """
    刪除預約
    """
    try:
        # 查詢預約
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({
                'success': False,
                'message': '找不到指定的預約'
            }), 404
        
        # 檢查權限（老師或學生可以刪除相關的預約）
        is_teacher = (hasattr(current_user, 'teacher') and 
                     current_user.teacher and 
                     booking.course.teacher_id == current_user.teacher.id)
        is_student = (hasattr(current_user, 'student') and 
                     current_user.student and 
                     booking.student_id == current_user.student.id)
        
        if not (is_teacher or is_student):
            return jsonify({
                'success': False,
                'message': '您沒有權限刪除此預約'
            }), 403
        
        # 刪除預約
        db.session.delete(booking)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '預約刪除成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'預約刪除失敗: {str(e)}'
        }), 500