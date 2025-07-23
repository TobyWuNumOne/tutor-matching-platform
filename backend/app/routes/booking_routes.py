from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.models.booking import Booking
from app.models.course import Course
from app.models.student import Student
from app.models.teacher import Teacher
from app.extensions import db
from datetime import datetime

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
                    },
                    'message': {
                        'type': 'string',
                        'description': '給老師的訊息（可選）',
                        'example': '希望能加強數學基礎'
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
                            'course': {
                                'type': 'object',
                                'properties': {
                                    'subject': {'type': 'string', 'example': '數學'},
                                    'teacher_name': {'type': 'string', 'example': '張老師'},
                                    'price': {'type': 'number', 'example': 800.0}
                                }
                            },
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
                    'message': {'type': 'string', 'example': '必填欄位不能為空'},
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
    學生建立預約
    """
    try:
        # 獲取請求資料
        data = request.get_json()
        
        # 驗證必填欄位
        required_fields = ['course_id', 'student_id', 'schedule_date']
        errors = {}
        
        for field in required_fields:
            if not data or field not in data or not data[field]:
                if field not in errors:
                    errors[field] = []
                
                field_names = {
                    'course_id': '課程ID',
                    'student_id': '學生ID',
                    'schedule_date': '預約時間'
                }
                errors[field].append(f'{field_names[field]}不能為空')
        
        # 驗證時間格式
        if data and 'schedule_date' in data and data['schedule_date']:
            try:
                datetime.strptime(data['schedule_date'], '%Y-%m-%d %H:%M')
            except ValueError:
                if 'schedule_date' not in errors:
                    errors['schedule_date'] = []
                errors['schedule_date'].append('預約時間格式錯誤，請使用 YYYY-MM-DD HH:MM 格式')
        
        # 如果有驗證錯誤，回傳錯誤訊息
        if errors:
            return jsonify({
                'success': False,
                'message': '必填欄位不能為空',
                'errors': errors
            }), 400
        
        # 檢查課程是否存在
        course = Course.query.get(data['course_id'])
        if not course:
            return jsonify({
                'success': False,
                'message': '指定的課程不存在'
            }), 404
        
        # 檢查學生是否存在
        student = Student.query.get(data['student_id'])
        if not student:
            return jsonify({
                'success': False,
                'message': '指定的學生不存在'
            }), 404
        
        # 檢查是否有時間衝突（同一個老師在同一時間的其他預約）
        existing_booking = Booking.query.join(Course).filter(
            Course.teacher_id == course.teacher_id,
            Booking.schedule_date == data['schedule_date'],
            Booking.status.in_(['pending', 'confirmed'])
        ).first()
        
        if existing_booking:
            return jsonify({
                'success': False,
                'message': '該時段已有其他預約，請選擇其他時間'
            }), 409
        
        # 建立新預約
        new_booking = Booking(
            course_id=data['course_id'],
            student_id=data['student_id'],
            schedule_date=data['schedule_date'],
            status='pending'
        )
        
        # 儲存到資料庫
        db.session.add(new_booking)
        db.session.commit()
        
        # 重新查詢以獲取關聯資料
        booking_with_relations = Booking.query.options(
            db.joinedload(Booking.course).joinedload(Course.teacher),
            db.joinedload(Booking.student)
        ).get(new_booking.id)
        
        # 回傳新建立的預約資料
        return jsonify({
            'success': True,
            'message': '預約申請已送出',
            'data': booking_with_relations.to_dict_with_relations()
        }), 201
        
    except Exception as e:
        # 如果發生錯誤，回滾交易
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'預約建立失敗: {str(e)}'
        }), 500


@booking_bp.route('/student/<int:student_id>', methods=['GET'])
@swag_from({
    'tags': ['預約管理'],
    'summary': '獲取學生的預約列表',
    'description': '獲取指定學生的所有預約記錄',
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
            'name': 'status',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': '預約狀態篩選',
            'enum': ['pending', 'confirmed', 'completed', 'cancelled'],
            'example': 'pending'
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
            'description': '成功獲取學生預約列表',
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
                                'schedule_date': {'type': 'string', 'example': '2024-07-25 14:30'},
                                'status': {'type': 'string', 'example': 'pending'},
                                'course': {
                                    'type': 'object',
                                    'properties': {
                                        'subject': {'type': 'string', 'example': '數學'},
                                        'teacher_name': {'type': 'string', 'example': '張老師'},
                                        'price': {'type': 'number', 'example': 800.0}
                                    }
                                }
                            }
                        }
                    },
                    'pagination': {
                        'type': 'object',
                        'properties': {
                            'page': {'type': 'integer', 'example': 1},
                            'per_page': {'type': 'integer', 'example': 10},
                            'total': {'type': 'integer', 'example': 15},
                            'pages': {'type': 'integer', 'example': 2}
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
                    'message': {'type': 'string', 'example': '指定的學生不存在'}
                }
            }
        }
    }
})
def get_student_bookings(student_id):
    """
    獲取學生的預約列表
    """
    try:
        # 檢查學生是否存在
        student = Student.query.get(student_id)
        if not student:
            return jsonify({
                'success': False,
                'message': '指定的學生不存在'
            }), 404
        
        # 獲取查詢參數
        status = request.args.get('status', '')
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)
        
        # 建立查詢
        query = Booking.query.filter_by(student_id=student_id).options(
            db.joinedload(Booking.course).joinedload(Course.teacher)
        )
        
        # 狀態篩選
        if status:
            query = query.filter(Booking.status == status)
        
        # 按建立時間降序排列
        query = query.order_by(Booking.created_at.desc())
        
        # 分頁查詢
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        bookings = pagination.items
        
        # 組建回應資料
        booking_list = [booking.to_dict_with_relations() for booking in bookings]
        
        return jsonify({
            'success': True,
            'data': booking_list,
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
            'message': f'獲取學生預約失敗: {str(e)}'
        }), 500


@booking_bp.route('/teacher/<int:teacher_id>', methods=['GET'])
@swag_from({
    'tags': ['預約管理'],
    'summary': '獲取老師的預約列表',
    'description': '獲取指定老師的所有預約記錄',
    'parameters': [
        {
            'name': 'teacher_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': '老師ID',
            'example': 1
        },
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
            'name': 'date_from',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': '開始日期（YYYY-MM-DD）',
            'example': '2024-07-01'
        },
        {
            'name': 'date_to',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': '結束日期（YYYY-MM-DD）',
            'example': '2024-07-31'
        }
    ],
    'responses': {
        200: {
            'description': '成功獲取老師預約列表',
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
                                'schedule_date': {'type': 'string', 'example': '2024-07-25 14:30'},
                                'status': {'type': 'string', 'example': 'pending'},
                                'student': {
                                    'type': 'object',
                                    'properties': {
                                        'name': {'type': 'string', 'example': '王同學'},
                                        'email': {'type': 'string', 'example': 'student@example.com'}
                                    }
                                },
                                'course': {
                                    'type': 'object',
                                    'properties': {
                                        'subject': {'type': 'string', 'example': '數學'},
                                        'price': {'type': 'number', 'example': 800.0}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        404: {
            'description': '老師不存在',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '指定的老師不存在'}
                }
            }
        }
    }
})
def get_teacher_bookings(teacher_id):
    """
    獲取老師的預約列表
    """
    try:
        # 檢查老師是否存在
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return jsonify({
                'success': False,
                'message': '指定的老師不存在'
            }), 404
        
        # 獲取查詢參數
        status = request.args.get('status', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        
        # 建立查詢 - 透過課程關聯找到老師的預約
        query = Booking.query.join(Course).filter(
            Course.teacher_id == teacher_id
        ).options(
            db.joinedload(Booking.course),
            db.joinedload(Booking.student)
        )
        
        # 狀態篩選
        if status:
            query = query.filter(Booking.status == status)
        
        # 日期範圍篩選
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
                query = query.filter(Booking.schedule_date >= date_from)
            except ValueError:
                pass
        
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
                # 加一天以包含當天的所有時間
                import datetime as dt
                date_to_end = (date_to_obj + dt.timedelta(days=1)).strftime('%Y-%m-%d')
                query = query.filter(Booking.schedule_date < date_to_end)
            except ValueError:
                pass
        
        # 按預約時間排序
        query = query.order_by(Booking.schedule_date.asc())
        
        bookings = query.all()
        
        # 組建回應資料
        booking_list = [booking.to_dict_with_relations() for booking in bookings]
        
        return jsonify({
            'success': True,
            'data': booking_list,
            'total': len(booking_list)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'獲取老師預約失敗: {str(e)}'
        }), 500


@booking_bp.route('/<int:booking_id>/status', methods=['PUT'])
@swag_from({
    'tags': ['預約管理'],
    'summary': '更新預約狀態',
    'description': '老師或學生更新預約狀態（確認、取消等）',
    'parameters': [
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
            'description': '狀態更新資訊',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {
                        'type': 'string',
                        'description': '新狀態',
                        'enum': ['pending', 'confirmed', 'completed', 'cancelled'],
                        'example': 'confirmed'
                    },
                    'reason': {
                        'type': 'string',
                        'description': '狀態變更原因（可選）',
                        'example': '時間確認無誤，期待上課'
                    }
                },
                'required': ['status']
            }
        }
    ],
    'responses': {
        200: {
            'description': '狀態更新成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': '預約狀態已更新'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'status': {'type': 'string', 'example': 'confirmed'},
                            'updated_at': {'type': 'string', 'example': '2024-07-23T10:30:00'}
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
def update_booking_status(booking_id):
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
        
        # 獲取請求資料
        data = request.get_json()
        
        if not data or 'status' not in data:
            return jsonify({
                'success': False,
                'message': '缺少必要的狀態參數'
            }), 400
        
        # 驗證狀態值
        valid_statuses = ['pending', 'confirmed', 'completed', 'cancelled']
        if data['status'] not in valid_statuses:
            return jsonify({
                'success': False,
                'message': f'無效的狀態值，可選值：{", ".join(valid_statuses)}'
            }), 400
        
        # 更新狀態
        booking.status = data['status']
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '預約狀態已更新',
            'data': {
                'id': booking.id,
                'status': booking.status,
                'updated_at': booking.updated_at.isoformat() if booking.updated_at else None
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'狀態更新失敗: {str(e)}'
        }), 500