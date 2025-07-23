from flask import Blueprint, request, jsonify
from flasgger import swag_from
from marshmallow import ValidationError
from app.models.teacher import Teacher
from app.models.user import User
from app.extensions import db
from app.schemas.teacher_schema import TeacherSchema, TeacherCreateSchema, TeacherUpdateSchema

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
        # 使用 Schema 驗證輸入資料
        schema = TeacherCreateSchema()
        data = schema.load(request.json)
        
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
        new_teacher = Teacher(**data)
        
        # 儲存到資料庫
        db.session.add(new_teacher)
        db.session.commit()
        
        # 使用 Schema 序列化輸出
        result_schema = TeacherSchema()
        return jsonify({
            'success': True,
            'message': '老師資料新增成功',
            'data': result_schema.dump(new_teacher)
        }), 201
        
    except ValidationError as err:
        return jsonify({
            'success': False,
            'message': '輸入資料驗證失敗',
            'errors': err.messages
        }), 400
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
        
        # 使用 Schema 序列化輸出
        schema = TeacherSchema()
        return jsonify({
            'success': True,
            'data': schema.dump(teacher)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'獲取老師資訊失敗: {str(e)}'
        }), 500