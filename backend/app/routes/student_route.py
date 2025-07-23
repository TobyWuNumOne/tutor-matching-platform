from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.models.student import Student
from app.models.user import User
from app.extensions import db

student_bp = Blueprint('students', __name__)

@student_bp.route('/create', methods=['POST'])
@swag_from({
    'tags': ['學生管理'],
    'summary': '新增學生資料',
    'description': '建立新的學生檔案，並與使用者帳號關聯',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': '學生資料',
            'schema': {
                'type': 'object',
                'properties': {
                    'user_id': {
                        'type': 'integer',
                        'description': '使用者ID（關聯到User表格）',
                        'example': 1
                    },
                    'email': {
                        'type': 'string',
                        'description': '學生電子郵件',
                        'example': 'student@example.com'
                    },
                    'gender': {
                        'type': 'string',
                        'description': '性別',
                        'enum': ['男', '女', '不願透露'],
                        'example': '男'
                    },
                    'age': {
                        'type': 'string',
                        'description': '年齡',
                        'example': '18'
                    }
                },
                'required': ['user_id', 'email']
            }
        }
    ],
    'responses': {
        201: {
            'description': '學生資料新增成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': '學生資料新增成功'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'user_id': {'type': 'integer', 'example': 1},
                            'email': {'type': 'string', 'example': 'student@example.com'},
                            'gender': {'type': 'string', 'example': '男'},
                            'age': {'type': 'string', 'example': '18'},
                            'created_at': {'type': 'string', 'example': '2024-01-01T10:00:00'},
                            'updated_at': {'type': 'string', 'example': '2024-01-01T10:00:00'}
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
                    'message': {'type': 'string', 'example': '必填欄位不能為空'},
                    'errors': {
                        'type': 'object',
                        'example': {
                            'email': ['電子郵件格式錯誤']
                        }
                    }
                }
            }
        },
        404: {
            'description': '使用者不存在',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '指定的使用者不存在'}
                }
            }
        },
        409: {
            'description': '學生資料已存在',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '該使用者已有學生資料'}
                }
            }
        },
        500: {
            'description': '伺服器錯誤',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '學生資料新增失敗'}
                }
            }
        }
    }
})
def create_student():
    """
    新增學生資料
    """
    try:
        # 獲取請求資料
        data = request.get_json()
        
        # 驗證必填欄位
        required_fields = ['user_id', 'email']
        errors = {}
        
        for field in required_fields:
            if not data or field not in data or not data[field]:
                if field not in errors:
                    errors[field] = []
                
                field_names = {
                    'user_id': '使用者ID',
                    'email': '電子郵件'
                }
                errors[field].append(f'{field_names[field]}不能為空')
        
        # 驗證電子郵件格式
        if data and 'email' in data and data['email']:
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, data['email']):
                if 'email' not in errors:
                    errors['email'] = []
                errors['email'].append('電子郵件格式錯誤')
        
        # 如果有驗證錯誤，回傳錯誤訊息
        if errors:
            return jsonify({
                'success': False,
                'message': '必填欄位不能為空',
                'errors': errors
            }), 400
        
        # 檢查使用者是否存在
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({
                'success': False,
                'message': '指定的使用者不存在'
            }), 404
        
        # 檢查該使用者是否已有學生資料
        existing_student = Student.query.filter_by(user_id=data['user_id']).first()
        if existing_student:
            return jsonify({
                'success': False,
                'message': '該使用者已有學生資料'
            }), 409
        
        # 建立新學生資料
        new_student = Student(
            user_id=data['user_id'],
            email=data['email'],
            gender=data.get('gender', ''),
            age=data.get('age', '')
        )
        
        # 儲存到資料庫
        db.session.add(new_student)
        db.session.commit()
        
        # 回傳新建立的學生資料
        return jsonify({
            'success': True,
            'message': '學生資料新增成功',
            'data': {
                'id': new_student.id,
                'user_id': new_student.user_id,
                'email': new_student.email,
                'gender': new_student.gender,
                'age': new_student.age,
                'created_at': new_student.created_at.isoformat() if new_student.created_at else None,
                'updated_at': new_student.updated_at.isoformat() if new_student.updated_at else None
            }
        }), 201
        
    except Exception as e:
        # 如果發生錯誤，回滾交易
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'學生資料新增失敗: {str(e)}'
        }), 500


@student_bp.route('/<int:student_id>', methods=['GET'])
@swag_from({
    'tags': ['學生管理'],
    'summary': '獲取學生詳細資訊',
    'description': '根據學生ID獲取詳細資訊，包含預約記錄統計',
    'parameters': [
        {
            'name': 'student_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': '學生ID',
            'example': 1
        },
        {
            'name': 'include_bookings',
            'in': 'query',
            'type': 'boolean',
            'required': False,
            'description': '是否包含預約記錄',
            'example': True
        }
    ],
    'responses': {
        200: {
            'description': '成功獲取學生詳細資訊',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'user_id': {'type': 'integer', 'example': 1},
                            'email': {'type': 'string', 'example': 'student@example.com'},
                            'gender': {'type': 'string', 'example': '男'},
                            'age': {'type': 'string', 'example': '18'},
                            'booking_stats': {
                                'type': 'object',
                                'properties': {
                                    'total_bookings': {'type': 'integer', 'example': 15},
                                    'pending_bookings': {'type': 'integer', 'example': 2},
                                    'confirmed_bookings': {'type': 'integer', 'example': 8},
                                    'completed_bookings': {'type': 'integer', 'example': 5}
                                }
                            },
                            'recent_bookings': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer', 'example': 1},
                                        'schedule_date': {'type': 'string', 'example': '2024-07-25 14:30'},
                                        'status': {'type': 'string', 'example': 'confirmed'},
                                        'course': {
                                            'type': 'object',
                                            'properties': {
                                                'subject': {'type': 'string', 'example': '數學'},
                                                'teacher_name': {'type': 'string', 'example': '張老師'}
                                            }
                                        }
                                    }
                                }
                            },
                            'created_at': {'type': 'string', 'example': '2024-01-01T10:00:00'},
                            'updated_at': {'type': 'string', 'example': '2024-01-01T10:00:00'}
                        }
                    }
                }
            }
        },
        404: {
            'description': '學生不存在',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '找不到指定的學生'}
                }
            }
        },
        500: {
            'description': '伺服器錯誤',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '獲取學生資訊失敗'}
                }
            }
        }
    }
})
def get_student_detail(student_id):
    """
    獲取學生詳細資訊
    """
    try:
        # 查詢學生資訊
        student = Student.query.get(student_id)
        
        if not student:
            return jsonify({
                'success': False,
                'message': '找不到指定的學生'
            }), 404
        
        # 基本學生資料
        student_data = {
            'id': student.id,
            'user_id': student.user_id,
            'email': student.email,
            'gender': student.gender,
            'age': student.age,
            'created_at': student.created_at.isoformat() if student.created_at else None,
            'updated_at': student.updated_at.isoformat() if student.updated_at else None
        }
        
        # 檢查是否需要包含預約資訊
        include_bookings = request.args.get('include_bookings', 'false').lower() == 'true'
        
        if include_bookings:
            # 獲取預約統計
            from app.models.booking import Booking
            from app.models.course import Course
            from sqlalchemy import func
            
            # 預約統計
            booking_stats = db.session.query(
                Booking.status,
                func.count(Booking.id).label('count')
            ).filter_by(student_id=student_id).group_by(Booking.status).all()
            
            stats = {
                'total_bookings': 0,
                'pending_bookings': 0,
                'confirmed_bookings': 0,
                'completed_bookings': 0,
                'cancelled_bookings': 0
            }
            
            for stat in booking_stats:
                stats['total_bookings'] += stat.count
                stats[f'{stat.status}_bookings'] = stat.count
            
            student_data['booking_stats'] = stats
            
            # 最近的預約記錄（最多5筆）
            recent_bookings = Booking.query.filter_by(student_id=student_id).options(
                db.joinedload(Booking.course).joinedload(Course.teacher)
            ).order_by(Booking.created_at.desc()).limit(5).all()
            
            recent_bookings_data = []
            for booking in recent_bookings:
                booking_data = {
                    'id': booking.id,
                    'schedule_date': booking.schedule_date,
                    'status': booking.status,
                    'course': {
                        'id': booking.course.id,
                        'subject': booking.course.subject,
                        'teacher_name': booking.course.teacher.name if booking.course.teacher else None
                    },
                    'created_at': booking.created_at.isoformat() if booking.created_at else None
                }
                recent_bookings_data.append(booking_data)
            
            student_data['recent_bookings'] = recent_bookings_data
        
        return jsonify({
            'success': True,
            'data': student_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'獲取學生資訊失敗: {str(e)}'
        }), 500


@student_bp.route('/user/<int:user_id>', methods=['GET'])
@swag_from({
    'tags': ['學生管理'],
    'summary': '根據使用者ID獲取學生資訊',
    'description': '根據使用者ID查找對應的學生資訊',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': '使用者ID',
            'example': 1
        }
    ],
    'responses': {
        200: {
            'description': '成功獲取學生資訊',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'user_id': {'type': 'integer', 'example': 1},
                            'email': {'type': 'string', 'example': 'student@example.com'},
                            'gender': {'type': 'string', 'example': '男'},
                            'age': {'type': 'string', 'example': '18'}
                        }
                    }
                }
            }
        },
        404: {
            'description': '找不到學生資訊',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '找不到對應的學生資訊'}
                }
            }
        }
    }
})
def get_student_by_user_id(user_id):
    """
    根據使用者ID獲取學生資訊
    """
    try:
        student = Student.query.filter_by(user_id=user_id).first()
        
        if not student:
            return jsonify({
                'success': False,
                'message': '找不到對應的學生資訊'
            }), 404
        
        student_data = {
            'id': student.id,
            'user_id': student.user_id,
            'email': student.email,
            'gender': student.gender,
            'age': student.age,
            'created_at': student.created_at.isoformat() if student.created_at else None,
            'updated_at': student.updated_at.isoformat() if student.updated_at else None
        }
        
        return jsonify({
            'success': True,
            'data': student_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'獲取學生資訊失敗: {str(e)}'
        }), 500


@student_bp.route('/auto-create', methods=['POST'])
@swag_from({
    'tags': ['學生管理'],
    'summary': '自動建立學生資料',
    'description': '在建立使用者時自動建立對應的學生資料（預設所有使用者都是學生）',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': '使用者基本資料',
            'schema': {
                'type': 'object',
                'properties': {
                    'user_id': {
                        'type': 'integer',
                        'description': '剛建立的使用者ID',
                        'example': 1
                    },
                    'email': {
                        'type': 'string',
                        'description': '使用者電子郵件',
                        'example': 'user@example.com'
                    },
                    'gender': {
                        'type': 'string',
                        'description': '性別（可選）',
                        'example': '男'
                    },
                    'age': {
                        'type': 'string',
                        'description': '年齡（可選）',
                        'example': '18'
                    }
                },
                'required': ['user_id', 'email']
            }
        }
    ],
    'responses': {
        201: {
            'description': '學生資料自動建立成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': '學生資料自動建立成功'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'user_id': {'type': 'integer', 'example': 1},
                            'email': {'type': 'string', 'example': 'user@example.com'}
                        }
                    }
                }
            }
        }
    }
})
def auto_create_student():
    """
    自動建立學生資料（用於使用者註冊後的預設建立）
    """
    try:
        data = request.get_json()
        
        # 檢查該使用者是否已有學生資料
        existing_student = Student.query.filter_by(user_id=data['user_id']).first()
        if existing_student:
            return jsonify({
                'success': True,
                'message': '學生資料已存在',
                'data': {
                    'id': existing_student.id,
                    'user_id': existing_student.user_id,
                    'email': existing_student.email
                }
            }), 200
        
        # 建立預設學生資料
        new_student = Student(
            user_id=data['user_id'],
            email=data['email'],
            gender=data.get('gender', ''),
            age=data.get('age', '')
        )
        
        db.session.add(new_student)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '學生資料自動建立成功',
            'data': {
                'id': new_student.id,
                'user_id': new_student.user_id,
                'email': new_student.email
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'學生資料自動建立失敗: {str(e)}'
        }), 500