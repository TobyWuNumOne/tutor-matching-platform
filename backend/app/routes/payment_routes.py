from flask import Blueprint, request, make_response, jsonify
from flasgger import swag_from
import hashlib
import urllib.parse
from datetime import datetime

from ..ecpay_test import main
from ..models import Payment, Teacher
from ..extensions import db

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/ecpay', methods=['GET', 'POST'])
@swag_from({
    'tags': ['綠界金流'],
    'summary': '老師藍勾勾認證付款',
    'description': 'GET: 測試付款頁面, POST: 建立藍勾勾認證付款訂單',
    'parameters': [
        {
            'name': 'teacher_id',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': '老師ID (POST 請求時使用)'
        },
        {
            'name': 'amount',
            'in': 'formData',
            'type': 'integer',
            'required': False,
            'description': '訂單費用 (POST 請求時使用)'
        },
        {
            'name': 'teacher_name',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': '老師姓名 (POST 請求時使用)'
        }
    ],
    'responses': {
        200: {
            'description': '成功回傳付款頁面或處理結果',
            'content': {
                'text/html': {
                    'schema': {'type': 'string'}
                }
            }
        }
    }
})
def ecpay_unified():
    """
    統一的老師藍勾勾認證付款處理端點
    GET: 用於測試，直接回傳綠界付款頁面
    POST: 用於建立認證訂單，接收老師資料後建立付款
    """
    try:
        if request.method == 'GET':
            # GET 請求：回傳測試付款頁面
            print("=== GET 請求：藍勾勾認證訂單測試付款 ===")
            html_content = main()
            response = make_response(html_content)
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
            return response
            
        elif request.method == 'POST':
            # POST 請求：處理老師認證資料並建立付款
            print("=== POST 請求：建立藍勾勾認證付款訂單 ===")
            
            # 正確處理不同的 Content-Type
            try:
                if request.is_json:
                    order_data = request.get_json()
                else:
                    order_data = request.form.to_dict()
            except Exception as e:
                print(f"❌ 解析請求資料失敗: {str(e)}")
                order_data = request.form.to_dict()
            
            print(f"收到訂單付款請求: {order_data}")
            
            # 驗證訂單資料 (可選)
            validated_data = validate_order_data(order_data)
            print(f"驗證後的訂單資料: {validated_data}")
            
            # 根據訂單資料建立付款 (目前還是使用固定的 main())
            html_content = process_payment_order(validated_data)
            response = make_response(html_content)
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
            return response
            
    except Exception as e:
        print(f"❌ 藍勾勾認證付款處理失敗: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'處理失敗: {str(e)}'
        }), 500

def validate_order_data(order_data):
    """驗證和處理老師認證資料"""
    try:
        # 處理老師 ID
        teacher_id = order_data.get('teacher_id')
        if teacher_id and teacher_id != 'DEFAULT_TEACHER':
            try:
                teacher_id = int(teacher_id)
                # 驗證老師是否存在
                teacher = Teacher.query.get(teacher_id)
                if not teacher:
                    raise ValueError(f'找不到老師 ID: {teacher_id}')
            except ValueError as e:
                if 'invalid literal' in str(e):
                    raise ValueError('老師 ID 必須是數字')
                raise e
        else:
            teacher_id = None  # 測試模式
            
        # 設定預設值
        validated_data = {
            'teacher_id': teacher_id,
            'amount': int(order_data.get('amount', 299)),  # 預設認證費用 299 元
            'teacher_name': order_data.get('teacher_name', '老師'),
            'teacher_phone': order_data.get('teacher_phone', ''),
            'description': order_data.get('description', '老師藍勾勾認證')
        }
        
        # 基本驗證
        if validated_data['amount'] <= 0:
            raise ValueError('認證費用必須大於 0')
        
        if not validated_data['teacher_name'].strip():
            raise ValueError('老師姓名不能為空')
            
        return validated_data
        
    except ValueError as e:
        raise e
    except Exception as e:
        raise ValueError(f'認證資料格式錯誤: {str(e)}')

def process_payment_order(order_data):
    """處理藍勾勾認證付款訂單資料並建立付款表單"""
    try:
        print(f"📝 處理藍勾勾認證付款訂單: {order_data}")
        
        # 記錄認證訂單資訊
        print(f"老師ID: {order_data['teacher_id']}")
        print(f"認證費用: {order_data['amount']}")
        print(f"老師姓名: {order_data['teacher_name']}")
        print(f"認證描述: {order_data['description']}")
        
        # TODO: 這裡可以在未來修改 main() 函數來接受動態參數
        # 目前先使用固定參數的 main() 函數
        html_content = main()
        
        print("✅ 藍勾勾認證付款表單建立成功")
        return html_content
        
    except Exception as e:
        print(f"❌ 處理藍勾勾認證付款訂單失敗: {str(e)}")
        raise e

@payment_bp.route('/result', methods=['POST'])
@swag_from({
    'tags': ['綠界金流'],
    'summary': '接收藍勾勾認證付款結果',
    'description': '綠界付款完成後的回傳網址，用於接收藍勾勾認證付款結果並驗證',
    'parameters': [
        {
            'name': 'MerchantID',
            'in': 'formData',
            'type': 'string',
            'description': '商店代號'
        },
        {
            'name': 'MerchantTradeNo',
            'in': 'formData',
            'type': 'string',
            'description': '商店訂單編號'
        },
        {
            'name': 'TradeNo',
            'in': 'formData',
            'type': 'string',
            'description': '綠界交易編號'
        },
        {
            'name': 'RtnCode',
            'in': 'formData',
            'type': 'string',
            'description': '回傳碼 (1=成功, 其他=失敗)'
        },
        {
            'name': 'RtnMsg',
            'in': 'formData',
            'type': 'string',
            'description': '回傳訊息'
        },
        {
            'name': 'PaymentDate',
            'in': 'formData',
            'type': 'string',
            'description': '付款時間'
        },
        {
            'name': 'TradeAmt',
            'in': 'formData',
            'type': 'string',
            'description': '交易金額'
        },
        {
            'name': 'CheckMacValue',
            'in': 'formData',
            'type': 'string',
            'description': '檢查碼'
        }
    ],
    'responses': {
        200: {
            'description': '成功接收付款結果',
            'schema': {
                'type': 'string',
                'example': '1|OK'
            }
        }
    }
})
def payment_result():
    """
    接收藍勾勾認證付款結果
    這個端點用作綠界的 ReturnURL，接收認證付款完成後的結果
    """
    try:
        print("=== 收到藍勾勾認證付款結果 ===")
        
        # 取得所有表單資料
        form_data = request.form.to_dict()
        print("訂單付款結果資料:", form_data)
        
        # 驗證必要欄位
        required_fields = ['MerchantID', 'MerchantTradeNo', 'TradeNo', 'RtnCode', 'CheckMacValue']
        missing_fields = [field for field in required_fields if field not in form_data]
        
        if missing_fields:
            print(f"❌ 缺少必要欄位: {missing_fields}")
            return "0|缺少必要欄位", 400
        
        # 驗證檢查碼...有需要嗎?
        # if verify_check_mac_value(form_data):
        #print("✅ 檢查碼驗證成功")
        
        # 取得付款結果資訊
        rtn_code = form_data.get('RtnCode')
        rtn_msg = form_data.get('RtnMsg', '')
        merchant_trade_no = form_data.get('MerchantTradeNo')
        trade_no = form_data.get('TradeNo')
        trade_amt = form_data.get('TradeAmt')
        payment_date = form_data.get('PaymentDate')
        payment_type = form_data.get('PaymentType', '')
        
        if rtn_code == '1':
            print(f"✅ 藍勾勾認證付款成功")
            print(f"商店訂單號: {merchant_trade_no}")
            print(f"綠界交易號: {trade_no}")
            print(f"認證費用: {trade_amt}")
            print(f"付款時間: {payment_date}")
            print(f"付款方式: {payment_type}")
            
            # 在這裡更新您的資料庫並啟用老師的藍勾勾認證
            update_payment_status(merchant_trade_no, 'paid', form_data)
            
        else:
            print(f"❌ 藍勾勾認證付款失敗: {rtn_msg}")
            print(f"錯誤代碼: {rtn_code}")
            
            # 在這裡更新您的資料庫為失敗狀態
            update_payment_status(merchant_trade_no, 'failed', form_data)
        
        # 回傳成功給綠界 (必須回傳 "1|OK")
        return "1|OK"
            
    except Exception as e:
        print(f"❌ 處理藍勾勾認證付款結果時發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()
        return "0|處理錯誤", 500

def update_payment_status(merchant_trade_no, status, payment_data):
    """更新藍勾勾認證付款狀態到資料庫"""
    try:
        print(f"更新認證訂單 {merchant_trade_no} 狀態為: {status}")
        print(f"認證付款資料: {payment_data}")
        
        # 查找或建立 Payment 記錄
        payment = Payment.query.filter_by(merchant_trade_no=merchant_trade_no).first()
        
        if not payment:
            # 如果沒有找到 Payment 記錄，建立一個新的藍勾勾認證訂單
            payment = Payment(
                merchant_trade_no=merchant_trade_no,
                total_amount=int(payment_data.get('TradeAmt', 0)),
                payment_status='PENDING',
                teacher_id=None,  # 這裡可能需要從其他地方獲取
                item_name='老師藍勾勾認證',
                trade_desc='尊貴藍勾勾認證服務'
            )
            db.session.add(payment)
            print(f"✅ 建立新的藍勾勾認證付款記錄: {merchant_trade_no}")
        
        # 更新付款狀態和綠界回傳的資料
        payment.payment_status = status
        payment.ecpay_trade_no = payment_data.get('TradeNo')
        payment.payment_date = datetime.now()
        payment.rtn_code = payment_data.get('RtnCode')
        payment.rtn_msg = payment_data.get('RtnMsg')
        payment.payment_method = payment_data.get('PaymentType')
        payment.payment_type_charge_fee = payment_data.get('PaymentTypeChargeFee', '0')
        
        # 如果付款成功，需要啟用老師的藍勾勾認證
        if status == 'paid' and payment.teacher_id:
            teacher = Teacher.query.get(payment.teacher_id)
            if teacher:
                teacher.blue_premium = True
                print(f"老師藍勾勾認證已啟用 (teacher_id: {payment.teacher_id}, name: {teacher.name})")
            else:
                print(f"找不到老師 ID: {payment.teacher_id}")
        elif status == 'paid':
            print(f"付款成功但沒有關聯的老師 ID")
        
        # 提交到資料庫
        db.session.commit()
        print(f"✅ 藍勾勾認證資料庫更新成功: {merchant_trade_no}")
        
        return True
        
    except Exception as e:
        print(f"❌ 藍勾勾認證資料庫更新失敗: {str(e)}")
        db.session.rollback()
        return False
        
    except Exception as e:
        print(f"❌ 更新資料庫失敗: {str(e)}")

@payment_bp.route('/status/<trade_no>', methods=['GET'])
@swag_from({
    'tags': ['綠界金流'],
    'summary': '查詢付款狀態',
    'parameters': [
        {
            'name': 'trade_no',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': '商店訂單編號'
        }
    ],
    'responses': {
        200: {
            'description': '成功查詢付款狀態',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'trade_no': {'type': 'string'},
                    'status': {'type': 'string'},
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def get_payment_status(trade_no):
    """查詢付款狀態"""
    try:
        # 這裡實作查詢邏輯
        # 暫時回傳範例資料
        return jsonify({
            'success': True,
            'trade_no': trade_no,
            'status': 'pending',  # pending, paid, failed
            'message': '查詢成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'查詢失敗: {str(e)}'
        }), 500

@payment_bp.route('/test', methods=['GET'])
def payment_test_page():
    """藍勾勾認證付款測試頁面"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>老師藍勾勾認證付款測試</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .form-group { margin: 15px 0; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, select { padding: 10px; width: 100%; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }
            .button { 
                padding: 12px 25px; 
                background: #007bff; 
                color: white; 
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                margin: 10px 5px;
                text-decoration: none;
                display: inline-block;
            }
            .button:hover { background: #0056b3; }
            .button.success { background: #28a745; }
            .button.success:hover { background: #1e7e34; }
            .button.premium { background: #6f42c1; }
            .button.premium:hover { background: #5a32a3; }
            .section { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
            .code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; font-family: monospace; }
            ul { padding-left: 20px; }
            li { margin: 5px 0; }
            .badge { 
                background: #6f42c1; 
                color: white; 
                padding: 2px 8px; 
                border-radius: 12px; 
                font-size: 12px; 
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔵 老師藍勾勾認證付款測試 <span class="badge">PREMIUM</span></h1>
            
            <div class="section">
                <h2>📝 測試表單 (POST 請求)</h2>
                <form action="/api/payment/ecpay" method="post">
                    <div class="form-group">
                        <label>老師ID:</label>
                        <input type="number" name="teacher_id" value="1" required>
                    </div>
                    
                    <div class="form-group">
                        <label>認證費用:</label>
                        <input type="number" name="amount" value="299" required>
                    </div>
                    
                    <div class="form-group">
                        <label>老師姓名:</label>
                        <input type="text" name="teacher_name" value="張老師" required>
                    </div>
                    
                    <div class="form-group">
                        <label>老師電話:</label>
                        <input type="tel" name="teacher_phone" value="0912345678">
                    </div>
                    
                    <div class="form-group">
                        <label>認證描述:</label>
                        <input type="text" name="description" value="老師藍勾勾認證" readonly>
                    </div>
                    
                    <button type="submit" class="button premium">建立藍勾勾認證訂單 (POST)</button>
                </form>
            </div>
            
            <div class="section">
                <h2>⚡ 快速測試 (GET 請求)</h2>
                <p>直接使用固定測試資料跳轉到綠界付款頁面：</p>
                <a href="/api/payment/ecpay" class="button success">直接測試認證付款 (GET)</a>
            </div>
            
            <div class="section">
                <h2>📋 API 端點說明</h2>
                <ul>
                    <li><strong>GET</strong> <code class="code">/api/payment/ecpay</code> - 測試認證付款頁面 (固定資料)</li>
                    <li><strong>POST</strong> <code class="code">/api/payment/ecpay</code> - 建立藍勾勾認證訂單 (動態資料)</li>
                    <li><strong>POST</strong> <code class="code">/api/payment/result</code> - 接收認證付款結果 (綠界回傳)</li>
                    <li><strong>GET</strong> <code class="code">/api/payment/status/&lt;trade_no&gt;</code> - 查詢認證付款狀態</li>
                    <li><strong>GET</strong> <code class="code">/api/payment/test</code> - 測試頁面 (本頁面)</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>📚 Swagger 文件</h2>
                <a href="/docs/" class="button">查看完整 API 文件</a>
            </div>
            
            <div class="section">
                <h2>🔄 藍勾勾認證流程</h2>
                <ol>
                    <li><strong>建立認證訂單：</strong>前端發送 POST 請求到 <code class="code">/api/payment/ecpay</code></li>
                    <li><strong>跳轉付款：</strong>系統回傳綠界付款頁面，老師完成認證費用付款</li>
                    <li><strong>接收結果：</strong>綠界發送付款結果到 <code class="code">/api/payment/result</code></li>
                    <li><strong>啟用認證：</strong>付款成功後自動啟用老師的藍勾勾認證</li>
                    <li><strong>查詢狀態：</strong>可通過 <code class="code">/api/payment/status/&lt;trade_no&gt;</code> 查詢</li>
                </ol>
            </div>
            
            <div class="section">
                <h2>💎 認證特色</h2>
                <ul>
                    <li>🔵 <strong>藍勾勾標誌：</strong>獲得平台官方認證標章</li>
                    <li>⭐ <strong>提升信任度：</strong>增加學生對老師的信任</li>
                    <li>📈 <strong>優先推薦：</strong>在搜尋結果中優先顯示</li>
                    <li>💰 <strong>一次付費：</strong>永久享有認證身份</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    '''