from flask import Blueprint, request, make_response, jsonify, render_template
from flasgger import swag_from
import hashlib
import re
from urllib.parse import quote_plus
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
            # GET 請求：回傳測試付款頁面（使用預設參數）
            print("=== GET 請求：藍勾勾認證訂單測試付款 ===")
            
            # 可以從 URL 參數獲取測試資料
            test_order_data = {
                'teacher_id': request.args.get('teacher_id'),
                'amount': int(request.args.get('amount', 299)),
                'teacher_name': request.args.get('teacher_name', '測試老師'),
                'teacher_phone': request.args.get('teacher_phone', '0912345678'),
                'description': request.args.get('description', '老師藍勾勾認證')
            }
            
            # 如果有 URL 參數，就轉換為綠界參數格式
            if any(test_order_data.values()):
                print(f"🔧 使用 URL 參數: {test_order_data}")
                order_params = convert_to_ecpay_params(test_order_data)
                html_content = main(order_params)
            else:
                print("🔧 使用預設測試參數")
                html_content = main()  # 不傳參數，使用預設值
            
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
            
            # 驗證訂單資料
            validated_data = validate_order_data(order_data)
            print(f"驗證後的訂單資料: {validated_data}")
            
            # 根據驗證後的資料建立付款
            html_content = process_payment_order(validated_data)
            response = make_response(html_content)
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
            return response
            
    except Exception as e:
        print(f"❌ 藍勾勾認證付款處理失敗: {str(e)}")
        import traceback
        traceback.print_exc()
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

def create_payment_record(order_params, order_data):
    """建立付款記錄到資料庫"""
    try:
        merchant_trade_no = order_params['MerchantTradeNo']
        
        # 檢查是否已存在相同的訂單編號
        existing_payment = Payment.query.filter_by(merchant_trade_no=merchant_trade_no).first()
        if existing_payment:
            print(f"⚠️  訂單編號已存在: {merchant_trade_no}")
            return existing_payment
        
        # 建立新的付款記錄
        payment = Payment(
            merchant_trade_no=merchant_trade_no,
            total_amount=int(order_params['TotalAmount']),
            payment_status='PENDING',  # 初始狀態為待付款
            teacher_id=order_data.get('teacher_id'),
            item_name=order_params['ItemName'],
            trade_desc=order_params['TradeDesc'],
            payment_method=None,  # 付款方式稍後由綠界回傳
            created_at=datetime.now(),
            payment_date=None,  # 付款完成時間稍後更新
            ecpay_trade_no=None,  # 綠界交易編號稍後更新
            rtn_code=None,
            rtn_msg=None,
            payment_type_charge_fee='0'
        )
        
        # 儲存到資料庫
        db.session.add(payment)
        db.session.commit()
        
        print(f"✅ 付款記錄已建立:")
        print(f"   訂單編號: {merchant_trade_no}")
        print(f"   老師ID: {order_data.get('teacher_id')}")
        print(f"   認證費用: {order_params['TotalAmount']} 元")
        print(f"   商品名稱: {order_params['ItemName']}")
        print(f"   資料庫ID: {payment.id}")
        
        return payment
        
    except Exception as e:
        print(f"❌ 建立付款記錄失敗: {str(e)}")
        db.session.rollback()
        return None

def convert_to_ecpay_params(order_data):
    """將前端訂單資料轉換為綠界 SDK 需要的參數格式"""
    try:
        # 🔧 統一訂單編號格式：使用時間戳記 (符合綠界 20 字元限制)
        merchant_trade_no = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # 取得老師 ID 用於記錄
        teacher_id = order_data.get('teacher_id')
        teacher_id_display = str(teacher_id) if teacher_id is not None else '測試'
        
        # 轉換為綠界 SDK 需要的格式
        ecpay_params = {
            'MerchantTradeNo': merchant_trade_no,
            'StoreID': '',
            'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            'PaymentType': 'aio',
            'TotalAmount': int(order_data.get('amount', 299)),
            'TradeDesc': order_data.get('description', '老師藍勾勾認證'),
            'ItemName': f"{order_data.get('teacher_name', '老師')}的藍勾勾認證服務",
            'ReturnURL': 'http://localhost:5000/api/payment/result',  # 付款完成後的回傳網址 (同步通知)
            #'NotifyURL': 'http://localhost:5000/api/payment/notify',  # 付款完成後的通知網址 (非同步通知)(正式環境才使用，需用外部可連線之網址)
            'ChoosePayment': 'Credit',
            'ItemURL': 'http://localhost:3000',  # 商品資訊頁面
            'Remark': f'老師ID: {teacher_id_display}',
            'ChooseSubPayment': '',
            
            # 🎯 付款完成後的跳轉頁面（帶上訂單編號）
            'ClientBackURL': f'http://localhost:3000/payment/success?trade_no={merchant_trade_no}',
            'OrderResultURL': f'http://localhost:3000/payment/result?trade_no={merchant_trade_no}',
            
            'NeedExtraPaidInfo': 'Y',
            'DeviceSource': '',
            'IgnorePayment': '',
            'PlatformID': '',
            'InvoiceMark': 'N',
            'CustomField1': teacher_id_display,  # 存放老師ID
            'CustomField2': order_data.get('teacher_phone', ''),    # 存放老師電話
            'CustomField3': '',
            'CustomField4': '',
            'EncryptType': 1,
        }
        
        print(f"🔄 訂單資料轉換:")
        print(f"   原始資料: {order_data}")
        print(f"   訂單編號: {merchant_trade_no} (長度: {len(merchant_trade_no)} 字元)")
        print(f"   老師姓名: {order_data.get('teacher_name')}")
        print(f"   認證費用: {order_data.get('amount')} 元")
        print(f"   老師ID: {teacher_id_display}")
        print(f"   ✅ 使用時間戳記訂單號格式")
        
        return ecpay_params
        
    except Exception as e:
        print(f"❌ 轉換綠界參數失敗: {str(e)}")
        raise e

def process_payment_order(order_data):
    """處理藍勾勾認證付款訂單資料並建立付款表單"""
    try:
        print(f"📝 處理藍勾勾認證付款訂單: {order_data}")
        
        # 記錄認證訂單資訊
        print(f"老師ID: {order_data['teacher_id']}")
        print(f"認證費用: {order_data['amount']}")
        print(f"老師姓名: {order_data['teacher_name']}")
        print(f"認證描述: {order_data['description']}")
        
        # 將 order_data 轉換為綠界 SDK 需要的 order_params 格式
        order_params = convert_to_ecpay_params(order_data)
        print(f"轉換後的綠界參數: {order_params}")
        
        # 🔥 重要：在建立綠界付款表單前，先將訂單記錄存入資料庫
        payment_record = create_payment_record(order_params, order_data)
        if not payment_record:
            raise Exception("建立付款記錄失敗")
        
        # 使用轉換後的參數建立付款表單
        html_content = main(order_params)
        
        print("✅ 藍勾勾認證付款表單建立成功")
        print(f"✅ 付款記錄已存入資料庫 (ID: {payment_record.id})")
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
    """接收藍勾勾認證付款結果"""
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
        
        # 先處理付款結果
        rtn_code = form_data.get('RtnCode')
        rtn_msg = form_data.get('RtnMsg', '')
        merchant_trade_no = form_data.get('MerchantTradeNo')
        trade_no = form_data.get('TradeNo')
        trade_amt = form_data.get('TradeAmt')
        payment_type = form_data.get('PaymentType')
        payment_date = form_data.get('PaymentDate')
        
        if rtn_code == '1':
            print(f"✅ 付款成功！")
            print(f"   商店訂單號: {merchant_trade_no}")
            print(f"   綠界交易號: {trade_no}")
            print(f"   付款金額: {trade_amt} 元")
            print(f"   付款方式: {payment_type}")
            print(f"   付款時間: {payment_date}")
            
            # 驗證 CheckMacValue（現在使用 SDK）
            try:
                if verify_check_mac_value(form_data):
                    print("✅ CheckMacValue 驗證成功")
                    verification_status = 'verified'
                else:
                    print("⚠️  CheckMacValue 驗證失敗，但付款已成功")
                    verification_status = 'paid_unverified'
            except Exception as e:
                print(f"⚠️  CheckMacValue 驗證過程出錯: {str(e)}")
                verification_status = 'paid_unverified'
            
            update_payment_status(merchant_trade_no, verification_status, form_data)
        else:
            print(f"❌ 付款失敗: {rtn_msg}")
            print(f"   錯誤代碼: {rtn_code}")
            update_payment_status(merchant_trade_no, 'failed', form_data)
        
        # 必須回傳 "1|OK" 給綠界
        return "1|OK"
        
    except Exception as e:
        print(f"❌ 處理付款結果失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return "0|處理錯誤", 500

def verify_check_mac_value(form_data):
    """驗證綠界付款回傳的 CheckMacValue - 使用 SDK 產生檢查碼"""
    try:
        # 動態載入綠界 SDK
        import importlib.util
        import os
        
        # 取得 SDK 路徑
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sdk_path = os.path.join(current_dir, '..', 'ecpay_payment_sdk.py')
        
        # 動態載入 SDK
        spec = importlib.util.spec_from_file_location("ecpay_payment_sdk", sdk_path)
        ecpay_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ecpay_module)
        
        # 建立 SDK 實例（使用測試環境參數）
        ecpay_sdk = ecpay_module.ECPayPaymentSdk(
            MerchantID='3002607',
            HashKey='pwFHCqoQZGmho4w6',  # 測試 HashKey
            HashIV='EkRm7iFT261dpevs'  # 測試 HashIV
        )
        
        # 取得綠界回傳的檢查碼
        received_check_mac = form_data.get('CheckMacValue', '')
        
        if not received_check_mac:
            print("❌ 沒有收到 CheckMacValue")
            return False
        
        # 複製表單資料並移除 CheckMacValue（SDK 會自動處理）
        params_copy = form_data.copy()
        if 'CheckMacValue' in params_copy:
            params_copy.pop('CheckMacValue')
        
        # 使用 SDK 產生檢查碼
        calculated_check_mac = ecpay_sdk.generate_check_value(params_copy)
        
        # Debug 資訊
        print(f"🔍 CheckMacValue 驗證 (使用 SDK)：")
        print(f"   參數數量: {len(params_copy)}")
        print(f"   主要參數: MerchantID={params_copy.get('MerchantID')}, TradeNo={params_copy.get('TradeNo')}")
        print(f"   收到的 CheckMacValue: {received_check_mac}")
        print(f"   SDK 計算的 CheckMacValue: {calculated_check_mac}")
        
        # 比較結果
        is_valid = calculated_check_mac == received_check_mac
        print(f"   驗證結果: {'✅ 成功' if is_valid else '❌ 失敗'}")
        
        if not is_valid:
            # 如果驗證失敗，顯示更詳細的 debug 資訊
            print(f"🔍 詳細 debug 資訊:")
            print(f"   所有參數: {params_copy}")
        
        return is_valid
        
    except Exception as e:
        print(f"❌ CheckMacValue 驗證過程發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def update_payment_status(merchant_trade_no, status, payment_data):
    """更新藍勾勾認證付款狀態到資料庫"""
    try:
        # 查找現有記錄
        payment = Payment.query.filter_by(merchant_trade_no=merchant_trade_no).first()
        
        # 🔥 更新付款狀態
        payment.payment_status = status  # ← 這裡更新狀態！
        payment.ecpay_trade_no = payment_data.get('TradeNo')
        payment.payment_date = datetime.now()
        payment.rtn_code = payment_data.get('RtnCode')
        payment.rtn_msg = payment_data.get('RtnMsg')
        payment.payment_method = payment_data.get('PaymentType')
        
        # 🔵 如果付款成功，啟用藍勾勾認證
        if status in ['paid', 'verified'] and payment.teacher_id:
            teacher = Teacher.query.get(payment.teacher_id)
            if teacher:
                teacher.blue_premium = True  # ← 啟用認證
        
        # 💾 提交到資料庫
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()

@payment_bp.route('/notify', methods=['POST'])
@swag_from({
    'tags': ['綠界金流'],
    'summary': '接收藍勾勾認證付款非同步通知',
    'description': '綠界付款完成後的非同步通知網址 (NotifyURL)，用於可靠地接收付款結果。這是綠界系統在付款完成後主動發送的通知，比同步回傳 (ReturnURL) 更可靠。',
    'parameters': [
        {
            'name': 'MerchantID',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': '商店代號'
        },
        {
            'name': 'MerchantTradeNo',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': '商店訂單編號'
        },
        {
            'name': 'TradeNo',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': '綠界交易編號'
        },
        {
            'name': 'RtnCode',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': '回傳碼 (1=成功, 其他=失敗)'
        },
        {
            'name': 'RtnMsg',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': '回傳訊息'
        },
        {
            'name': 'PaymentDate',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': '付款時間 (格式: YYYY/MM/DD HH:mm:ss)'
        },
        {
            'name': 'TradeAmt',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': '交易金額'
        },
        {
            'name': 'PaymentType',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': '付款方式 (Credit_CreditCard, ATM_ESUN, CVS_CVS 等)'
        },
        {
            'name': 'TradeDate',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': '訂單建立時間'
        },
        {
            'name': 'CheckMacValue',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': '檢查碼，用於驗證資料完整性'
        },
        {
            'name': 'SimulatePaid',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': '模擬付款 (測試環境用)'
        }
    ],
    'responses': {
        200: {
            'description': '成功接收並處理付款通知',
            'schema': {
                'type': 'string',
                'example': '1|OK'
            }
        },
        400: {
            'description': '缺少必要欄位或資料驗證失敗',
            'schema': {
                'type': 'string',
                'example': '0|缺少必要欄位'
            }
        },
        500: {
            'description': '伺服器內部錯誤',
            'schema': {
                'type': 'string',
                'example': '0|處理錯誤'
            }
        }
    }
})
def payment_notify():
    """接收藍勾勾認證付款非同步通知 (NotifyURL)"""
    try:
        print("=== 🔔 收到藍勾勾認證付款非同步通知 (NotifyURL) ===")
        
        # 取得所有表單資料
        form_data = request.form.to_dict()
        print("📥 非同步通知資料:", form_data)
        
        # 驗證必要欄位
        required_fields = ['MerchantID', 'MerchantTradeNo', 'TradeNo', 'RtnCode', 'CheckMacValue']
        missing_fields = [field for field in required_fields if field not in form_data]
        
        if missing_fields:
            print(f"❌ 非同步通知缺少必要欄位: {missing_fields}")
            return "0|缺少必要欄位", 400
        
        # 取得重要欄位
        rtn_code = form_data.get('RtnCode')
        rtn_msg = form_data.get('RtnMsg', '')
        merchant_trade_no = form_data.get('MerchantTradeNo')
        trade_no = form_data.get('TradeNo')
        trade_amt = form_data.get('TradeAmt')
        payment_type = form_data.get('PaymentType')
        payment_date = form_data.get('PaymentDate')
        
        print(f"📋 非同步通知詳細資料:")
        print(f"   商店訂單號: {merchant_trade_no}")
        print(f"   綠界交易號: {trade_no}")
        print(f"   回傳碼: {rtn_code}")
        print(f"   回傳訊息: {rtn_msg}")
        print(f"   付款金額: {trade_amt}")
        print(f"   付款方式: {payment_type}")
        print(f"   付款時間: {payment_date}")
        
        # 檢查該訂單是否存在
        payment_record = Payment.query.filter_by(merchant_trade_no=merchant_trade_no).first()
        if not payment_record:
            print(f"⚠️  找不到訂單記錄: {merchant_trade_no}")
            return "0|訂單不存在", 400
        
        # 處理付款結果
        if rtn_code == '1':
            print(f"✅ 非同步通知: 付款成功！")
            print(f"   當前訂單狀態: {payment_record.payment_status}")
            
            # 驗證 CheckMacValue
            try:
                if verify_check_mac_value(form_data):
                    print("✅ 非同步通知 CheckMacValue 驗證成功")
                    verification_status = 'verified'
                    update_payment_status(merchant_trade_no, verification_status, form_data)
                    print(f"🔵 付款成功，已啟用老師 {payment_record.teacher_id} 的藍勾勾認證")
                else:
                    print("⚠️  非同步通知 CheckMacValue 驗證失敗，但付款已成功")
                    verification_status = 'paid_unverified'
                    update_payment_status(merchant_trade_no, verification_status, form_data)
            except Exception as e:
                print(f"⚠️  非同步通知 CheckMacValue 驗證過程出錯: {str(e)}")
                verification_status = 'paid_unverified'
                update_payment_status(merchant_trade_no, verification_status, form_data)
        else:
            print(f"❌ 非同步通知: 付款失敗")
            print(f"   錯誤代碼: {rtn_code}")
            print(f"   錯誤訊息: {rtn_msg}")
            update_payment_status(merchant_trade_no, 'failed', form_data)
        
        # 非同步通知必須回傳 "1|OK" 給綠界，表示已成功接收
        print("✅ 非同步通知處理完成，回傳確認給綠界")
        return "1|OK"
        
    except Exception as e:
        print(f"❌ 處理非同步通知失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # 即使處理失敗，也要回傳錯誤狀態給綠界
        return "0|處理錯誤", 500

@payment_bp.route('/status/<trade_no>', methods=['GET'])
@swag_from({
    'tags': ['綠界金流'],
    'summary': '查詢藍勾勾認證付款狀態',
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
                    'teacher_verified': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def get_payment_status(trade_no):
    """查詢藍勾勾認證付款狀態"""
    try:
        # 查詢 Payment 記錄
        payment = Payment.query.filter_by(merchant_trade_no=trade_no).first()
        
        if payment:
            # 檢查老師是否已啟用藍勾勾認證
            teacher_verified = False
            teacher_name = None
            if payment.teacher_id:
                teacher = Teacher.query.get(payment.teacher_id)
                if teacher:
                    teacher_verified = getattr(teacher, 'blue_premium', False)
                    teacher_name = getattr(teacher, 'name', None)
            
            return jsonify({
                'success': True,
                'trade_no': trade_no,
                'status': payment.payment_status,
                'amount': payment.total_amount,
                'teacher_id': payment.teacher_id,
                'teacher_name': teacher_name,
                'teacher_verified': teacher_verified,
                'ecpay_trade_no': payment.ecpay_trade_no,
                'payment_date': payment.payment_date.isoformat() if payment.payment_date else None,
                'created_at': payment.created_at.isoformat() if hasattr(payment, 'created_at') and payment.created_at else None,
                'item_name': payment.item_name,
                'message': '查詢成功'
            }), 200
        else:
            return jsonify({
                'success': False,
                'trade_no': trade_no,
                'status': 'not_found',
                'message': '找不到該認證訂單'
            }), 404
        
    except Exception as e:
        print(f"❌ 查詢付款狀態失敗: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'查詢失敗: {str(e)}'
        }), 500

@payment_bp.route('/test', methods=['GET'])
def payment_test_page():
    """藍勾勾認證付款測試頁面"""
    return render_template('test.html')