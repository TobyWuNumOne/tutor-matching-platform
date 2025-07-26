from flask import Blueprint, request, make_response, jsonify
from flasgger import swag_from
import hashlib
import urllib.parse
from datetime import datetime

# # 如果 main 函數在其他地方，請調整導入路徑
# try:
from ..ecpay_test import main
# except ImportError:
#     # 如果在根目錄，使用相對導入
#     import sys
#     import os
#     sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    # from payment import ecpay, order_search  # 使用您現有的函數

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/ecpay', methods=['GET', 'POST'])
@swag_from({
    'tags': ['綠界金流'],
    'summary': '綠界金流處理',
    'description': '處理綠界金流相關請求',
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
def ecpay_view():
    """綠界金流視圖"""
    try:
        html_content = main()
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'綠界金流處理失敗: {str(e)}'
        }), 500

# 如果需要其他綠界相關路由
@payment_bp.route('/create_payment', methods=['POST'])
def create_payment():
    """建立付款訂單"""
    try:
        order_data = request.get_json() or request.form.to_dict()
        print(f"收到付款請求: {order_data}")
        
        # 直接使用 main() 函數
        html_content = main()
        return make_response(html_content)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'建立付款失敗: {str(e)}'
        }), 500
@payment_bp.route('/result', methods=['POST'])
@swag_from({
    'tags': ['綠界金流'],
    'summary': '接收綠界付款結果',
    'description': '綠界付款完成後的回傳網址，用於接收付款結果並驗證',
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
    接收綠界付款結果
    這個端點用作綠界的 ReturnURL，接收付款完成後的結果
    """
    try:
        print("=== 收到綠界付款結果 ===")
        
        # 取得所有表單資料
        form_data = request.form.to_dict()
        print("付款結果資料:", form_data)
        
        # 驗證必要欄位
        required_fields = ['MerchantID', 'MerchantTradeNo', 'TradeNo', 'RtnCode', 'CheckMacValue']
        missing_fields = [field for field in required_fields if field not in form_data]
        
        if missing_fields:
            print(f"❌ 缺少必要欄位: {missing_fields}")
            return "0|缺少必要欄位", 400
        
        # 驗證檢查碼
        if verify_check_mac_value(form_data):
            print("✅ 檢查碼驗證成功")
            
            # 取得付款結果資訊
            rtn_code = form_data.get('RtnCode')
            rtn_msg = form_data.get('RtnMsg', '')
            merchant_trade_no = form_data.get('MerchantTradeNo')
            trade_no = form_data.get('TradeNo')
            trade_amt = form_data.get('TradeAmt')
            payment_date = form_data.get('PaymentDate')
            payment_type = form_data.get('PaymentType', '')
            
            if rtn_code == '1':
                print(f"✅ 付款成功")
                print(f"商店訂單號: {merchant_trade_no}")
                print(f"綠界交易號: {trade_no}")
                print(f"付款金額: {trade_amt}")
                print(f"付款時間: {payment_date}")
                print(f"付款方式: {payment_type}")
                
                # 在這裡更新您的資料庫
                update_payment_status(merchant_trade_no, 'paid', form_data)
                
            else:
                print(f"❌ 付款失敗: {rtn_msg}")
                print(f"錯誤代碼: {rtn_code}")
                
                # 在這裡更新您的資料庫為失敗狀態
                update_payment_status(merchant_trade_no, 'failed', form_data)
            
            # 回傳成功給綠界 (必須回傳 "1|OK")
            return "1|OK"
            
        else:
            print("❌ 檢查碼驗證失敗")
            return "0|檢查碼驗證失敗", 400
            
    except Exception as e:
        print(f"❌ 處理付款結果時發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()
        return "0|處理錯誤", 500

def verify_check_mac_value(form_data):
    """驗證綠界回傳的檢查碼"""
    try:
        # 綠界測試環境的金鑰 (請替換為您的正式金鑰)
        HASH_KEY = 'pwFHCqoQZGmho4w6'  # 測試用
        HASH_IV = 'EkRm7iFT261dpevs'   # 測試用
        
        # 取得收到的檢查碼
        received_check_mac = form_data.get('CheckMacValue', '')
        
        # 移除 CheckMacValue 後重新計算
        check_data = {k: v for k, v in form_data.items() if k != 'CheckMacValue'}
        
        # 按照 key 排序
        sorted_params = sorted(check_data.items())
        
        # 組合字串
        raw_string = '&'.join([f'{k}={v}' for k, v in sorted_params])
        raw_string = f'HashKey={HASH_KEY}&{raw_string}&HashIV={HASH_IV}'
        
        print(f"檢查碼計算字串: {raw_string}")
        
        # URL encode 並轉小寫
        encoded_string = urllib.parse.quote_plus(raw_string).lower()
        print(f'encode後:{encoded_string}')
        
        # sha256 加密並轉大寫
        calculated_check_mac = hashlib.sha256(encoded_string.encode('utf-8')).hexdigest().upper()
        
        print(f"計算的檢查碼: {calculated_check_mac}")
        print(f"收到的檢查碼: {received_check_mac}")
        
        return received_check_mac.upper() == calculated_check_mac.upper()
        
    except Exception as e:
        print(f"驗證檢查碼時發生錯誤: {str(e)}")
        return False

def update_payment_status(merchant_trade_no, status, payment_data):
    """更新付款狀態到資料庫"""
    try:
        # 這裡實作您的資料庫更新邏輯
        print(f"更新訂單 {merchant_trade_no} 狀態為: {status}")
        
        # 範例：如果您有 Payment 模型
        # from app.models.payment import Payment
        # from app.extensions import db
        # 
        # payment = Payment.query.filter_by(trade_no=merchant_trade_no).first()
        # if payment:
        #     payment.payment_status = status
        #     payment.ecpay_trade_no = payment_data.get('TradeNo')
        #     payment.payment_date = datetime.now()
        #     payment.rtn_code = payment_data.get('RtnCode')
        #     payment.rtn_msg = payment_data.get('RtnMsg')
        #     payment.payment_method = payment_data.get('PaymentType')
        #     db.session.commit()
        #     print(f"✅ 資料庫更新成功")
        
        # 暫時只記錄 log
        print(f"付款資料: {payment_data}")
        
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