from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.models.teacher import Teacher
from app.models.user import User
from app.extensions import db

teacher_bp = Blueprint('teachers', __name__)

@teacher_bp.route('/create', methods=['POST'])
@swag_from({
    'tags': ['老師管理'],
    'summary': '新增老師資料',
    'description': '建立新的老師檔案，並與使用者帳號關聯',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': '老師資料',
            'schema': {
                'type': 'object',
                'properties': {
                    'user_id': {
                        'type': 'integer',
                        'description': '使用者ID（關聯到User表格）',
                        'example': 1
                    },
                    'avatar': {
                        'type': 'string',
                        'description': '老師頭像URL',
                        'example': 'https://example.com/avatar.jpg'
                    },
                    'name': {
                        'type': 'string',
                        'description': '老師姓名',
                        'example': '張老師'
                    },
                    'email': {
                        'type': 'string',
                        'description': '老師電子郵件',
                        'example': 'teacher@example.com'
                    },
                    'phone': {
                        'type': 'string',
                        'description': '聯絡電話',
                        'example': '0912345678'
                    },
                    'gender': {
                        'type': 'string',
                        'description': '性別',
                        'enum': ['男', '女', '不願透露'],
                        'example': '女'
                    },
                    'age': {
                        'type': 'string',
                        'description': '年齡',
                        'example': '30'
                    },
                    'education': {
                        'type': 'string',
                        'description': '學歷',
                        'example': '台灣大學數學系碩士'
                    },
                    'certifications': {
                        'type': 'string',
                        'description': '證照與認證',
                        'example': '中等學校數學科教師證, 數學奧林匹亞指導員證'
                    },
                    'intro': {
                        'type': 'string',
                        'description': '自我介紹',
                        'example': '我是張老師，擁有10年數學教學經驗，擅長啟發式教學。'
                    },
                    'teaching_experience': {
                        'type': 'string',
                        'description': '教學經驗',
                        'example': '曾任建中數學老師5年，私人家教經驗10年，學生升學率95%以上。'
                    },
                    'status': {
                        'type': 'string',
                        'description': '老師狀態',
                        'enum': ['active', 'inactive', 'pending'],
                        'example': 'active'
                    },
                    'blue_premium': {
                        'type': 'boolean',
                        'description': '是否為藍鑽會員',
                        'example': False
                    }
                },
                'required': ['user_id', 'name', 'email', 'education', 'certifications', 'intro', 'teaching_experience']
            }
        }
    ],
    'responses': {
        201: {
            'description': '老師資料新增成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': '老師資料新增成功'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'user_id': {'type': 'integer', 'example': 1},
                            'avatar': {'type': 'string', 'example': 'https://example.com/avatar.jpg'},
                            'name': {'type': 'string', 'example': '張老師'},
                            'email': {'type': 'string', 'example': 'teacher@example.com'},
                            'phone': {'type': 'string', 'example': '0912345678'},
                            'gender': {'type': 'string', 'example': '女'},
                            'age': {'type': 'string', 'example': '30'},
                            'education': {'type': 'string', 'example': '台灣大學數學系碩士'},
                            'certifications': {'type': 'string', 'example': '中等學校數學科教師證'},
                            'intro': {'type': 'string', 'example': '我是張老師，擁有10年數學教學經驗'},
                            'teaching_experience': {'type': 'string', 'example': '曾任建中數學老師5年'},
                            'status': {'type': 'string', 'example': 'active'},
                            'blue_premium': {'type': 'boolean', 'example': False},
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
                            'name': ['老師姓名不能為空'],
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
            'description': '老師資料已存在',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '該使用者已有老師資料'}
                }
            }
        },
        500: {
            'description': '伺服器錯誤',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '老師資料新增失敗'}
                }
            }
        }
    }
})
def create_teacher():
    """
    新增老師資料
    """
    try:
        # 獲取請求資料
        data = request.get_json()
        
        # 驗證必填欄位
        required_fields = ['user_id', 'name', 'email', 'education', 'certifications', 'intro', 'teaching_experience']
        errors = {}
        
        for field in required_fields:
            if not data or field not in data or not data[field]:
                if field not in errors:
                    errors[field] = []
                
                field_names = {
                    'user_id': '使用者ID',
                    'name': '老師姓名',
                    'email': '電子郵件',
                    'education': '學歷',
                    'certifications': '證照與認證',
                    'intro': '自我介紹',
                    'teaching_experience': '教學經驗'
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
        
        # 檢查該使用者是否已有老師資料
        existing_teacher = Teacher.query.filter_by(user_id=data['user_id']).first()
        if existing_teacher:
            return jsonify({
                'success': False,
                'message': '該使用者已有老師資料'
            }), 409
        
        # 建立新老師資料
        new_teacher = Teacher(
            user_id=data['user_id'],
            avatar=data.get('avatar', ''),
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            gender=data.get('gender', ''),
            age=data.get('age', ''),
            education=data['education'],
            certifications=data['certifications'],
            intro=data['intro'],
            teaching_experience=data['teaching_experience'],
            status=data.get('status', 'active'),
            blue_premium=data.get('blue_premium', False)
        )
        
        # 儲存到資料庫
        db.session.add(new_teacher)
        db.session.commit()
        
        # 回傳新建立的老師資料
        return jsonify({
            'success': True,
            'message': '老師資料新增成功',
            'data': {
                'id': new_teacher.id,
                'user_id': new_teacher.user_id,
                'avatar': new_teacher.avatar,
                'name': new_teacher.name,
                'email': new_teacher.email,
                'phone': new_teacher.phone,
                'gender': new_teacher.gender,
                'age': new_teacher.age,
                'education': new_teacher.education,
                'certifications': new_teacher.certifications,
                'intro': new_teacher.intro,
                'teaching_experience': new_teacher.teaching_experience,
                'status': new_teacher.status,
                'blue_premium': new_teacher.blue_premium,
                'created_at': new_teacher.created_at.isoformat() if new_teacher.created_at else None,
                'updated_at': new_teacher.updated_at.isoformat() if new_teacher.updated_at else None
            }
        }), 201
        
    except Exception as e:
        # 如果發生錯誤，回滾交易
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'老師資料新增失敗: {str(e)}'
        }), 500

@teacher_bp.route('/name/<string:teacher_name>', methods=['GET'])
@swag_from({
    'tags': ['老師管理'],
    'summary': '根據老師姓名獲取詳細資訊',
    'description': '根據老師姓名獲取詳細資訊，包含相關課程',
    'parameters': [
        {
            'name': 'teacher_name',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': '老師姓名',
            'example': '張老師'
        }
    ],
    'responses': {
        200: {
            'description': '成功獲取老師詳細資訊',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'user_id': {'type': 'integer', 'example': 1},
                            'avatar': {'type': 'string', 'example': 'https://example.com/avatar.jpg'},
                            'name': {'type': 'string', 'example': '張老師'},
                            'email': {'type': 'string', 'example': 'teacher@example.com'},
                            'phone': {'type': 'string', 'example': '0912345678'},
                            'gender': {'type': 'string', 'example': '女'},
                            'age': {'type': 'string', 'example': '30'},
                            'education': {'type': 'string', 'example': '台灣大學數學系碩士'},
                            'certifications': {'type': 'string', 'example': '中等學校數學科教師證'},
                            'intro': {'type': 'string', 'example': '我是張老師，擁有10年數學教學經驗'},
                            'teaching_experience': {'type': 'string', 'example': '曾任建中數學老師5年'},
                            'status': {'type': 'string', 'example': 'active'},
                            'blue_premium': {'type': 'boolean', 'example': False},
                            'courses': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'integer', 'example': 1},
                                        'subject': {'type': 'string', 'example': '數學'},
                                        'description': {'type': 'string', 'example': '高中數學課程'},
                                        'price': {'type': 'number', 'example': 800.0},
                                        'location': {'type': 'string', 'example': '台北'},
                                        'avg_rating': {'type': 'number', 'example': 4.5}
                                    }
                                }
                            },
                            'created_at': {'type': 'string', 'example': '2024-01-01T10:00:00'}
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
                    'message': {'type': 'string', 'example': '找不到指定的老師'}
                }
            }
        },
        500: {
            'description': '伺服器錯誤',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '獲取老師資訊失敗'}
                }
            }
        }
    }
})
def get_teacher_by_name(teacher_name):
    """
    根據老師姓名獲取詳細資訊
    """
    try:
        # URL decode 處理中文名稱
        from urllib.parse import unquote
        decoded_name = unquote(teacher_name)
        
        # 查詢老師資訊，包含關聯的課程
        from sqlalchemy.orm import joinedload
        teacher = Teacher.query.options(joinedload(Teacher.courses)).filter_by(name=decoded_name).first()
        
        if not teacher:
            return jsonify({
                'success': False,
                'message': '找不到指定的老師'
            }), 404
        
        # 組建課程資訊
        courses_data = []
        if hasattr(teacher, 'courses'):
            for course in teacher.courses:
                course_data = {
                    'id': course.id,
                    'subject': course.subject,
                    'description': course.description,
                    'price': float(course.price) if course.price else None,
                    'location': course.location,
                    'avg_rating': course.avg_rating,
                    'created_at': course.created_at.isoformat() if course.created_at else None
                }
                courses_data.append(course_data)
        
        # 組建回應資料
        teacher_data = {
            'id': teacher.id,
            'user_id': teacher.user_id,
            'avatar': teacher.avatar,
            'name': teacher.name,
            'email': teacher.email,
            'phone': teacher.phone,
            'gender': teacher.gender,
            'age': teacher.age,
            'education': teacher.education,
            'certifications': teacher.certifications,
            'intro': teacher.intro,
            'teaching_experience': teacher.teaching_experience,
            'status': teacher.status,
            'blue_premium': teacher.blue_premium,
            'courses': courses_data,
            'created_at': teacher.created_at.isoformat() if teacher.created_at else None,
            'updated_at': teacher.updated_at.isoformat() if teacher.updated_at else None
        }
        
        return jsonify({
            'success': True,
            'data': teacher_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'獲取老師資訊失敗: {str(e)}'
        }), 500