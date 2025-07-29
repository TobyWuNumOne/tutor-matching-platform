#!/usr/bin/env python3
"""
綠界金流訂單診斷工具
用於檢查為什麼綠界後台沒有顯示訂單
"""

import sys
import os
sys.path.append('.')

from datetime import datetime
from app.routes.payment_routes import convert_to_ecpay_params
from app.ecpay_test import main

def diagnose_ecpay_order():
    print("=== 🔍 綠界訂單診斷工具 ===")
    print()
    
    # 1. 檢查訂單號格式
    print("1️⃣ 檢查訂單號格式:")
    trade_no = datetime.now().strftime("%Y%m%d%H%M%S")
    print(f"   訂單號: {trade_no}")
    print(f"   長度: {len(trade_no)} 字元")
    print(f"   ✅ 符合綠界要求 (≤20字元)" if len(trade_no) <= 20 else f"   ❌ 超過長度限制")
    print()
    
    # 2. 測試訂單參數生成
    print("2️⃣ 測試訂單參數生成:")
    test_order_data = {
        'teacher_id': 1,
        'amount': 299,
        'teacher_name': '測試老師',
        'teacher_phone': '0912345678',
        'description': '老師藍勾勾認證'
    }
    
    try:
        ecpay_params = convert_to_ecpay_params(test_order_data)
        print(f"   ✅ 參數生成成功")
        print(f"   訂單編號: {ecpay_params['MerchantTradeNo']}")
        print(f"   商品名稱: {ecpay_params['ItemName']}")
        print(f"   交易金額: {ecpay_params['TotalAmount']}")
        print(f"   付款方式: {ecpay_params['ChoosePayment']}")
    except Exception as e:
        print(f"   ❌ 參數生成失敗: {e}")
        return
    print()
    
    # 3. 檢查綠界 SDK 設定
    print("3️⃣ 檢查綠界 SDK 設定:")
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("ecpay_payment_sdk", "app/ecpay_payment_sdk.py")
        ecpay_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ecpay_module)
        
        sdk = ecpay_module.ECPayPaymentSdk(
            MerchantID='3002607',
            HashKey='pwFHCqoQZGmho4w6',
            HashIV='EkRm7iFT261dpevs'
        )
        print(f"   ✅ SDK 載入成功")
        print(f"   商店ID: 3002607 (測試環境)")
        print(f"   HashKey: pwFHC*** (已設定)")
        print(f"   HashIV: EkRm7*** (已設定)")
    except Exception as e:
        print(f"   ❌ SDK 載入失敗: {e}")
        return
    print()
    
    # 4. 測試完整流程
    print("4️⃣ 測試完整付款流程:")
    try:
        html_content = main(ecpay_params)
        print(f"   ✅ 付款表單生成成功")
        print(f"   HTML 長度: {len(html_content)} 字元")
        
        # 檢查 HTML 中的關鍵資訊
        if ecpay_params['MerchantTradeNo'] in html_content:
            print(f"   ✅ 訂單編號已包含在表單中")
        else:
            print(f"   ❌ 訂單編號未包含在表單中")
            
        if 'payment-stage.ecpay.com.tw' in html_content:
            print(f"   ✅ 使用測試環境網址")
        else:
            print(f"   ⚠️  可能使用正式環境網址")
            
    except Exception as e:
        print(f"   ❌ 付款表單生成失敗: {e}")
        return
    print()
    
    # 5. 可能的問題診斷
    print("5️⃣ 可能的問題診斷:")
    print("   💡 如果綠界後台沒有訂單，可能原因：")
    print()
    print("   🔸 付款流程未完成:")
    print("      - 訂單只有在用戶實際點擊付款時才會出現在綠界後台")
    print("      - 請確認是否有實際進行付款測試")
    print()
    print("   🔸 測試環境問題:")
    print("      - 確認使用的是綠界測試環境帳號")
    print("      - 測試商店ID: 3002607")
    print("      - 登入測試後台: https://vendor-stage.ecpay.com.tw/")
    print()
    print("   🔸 網路連線問題:")
    print("      - 確認伺服器可以連接到綠界測試環境")
    print("      - 檢查防火牆設定")
    print()
    
    # 6. 建議解決步驟
    print("6️⃣ 建議解決步驟:")
    print("   1. 前往 http://localhost:5000/api/payment/test")
    print("   2. 使用測試表單建立訂單")
    print("   3. 實際完成付款流程 (使用測試信用卡)")
    print("   4. 檢查綠界測試後台是否出現訂單")
    print("   5. 如果還是沒有，檢查伺服器日誌")
    print()
    
    print("✅ 診斷完成！")

if __name__ == "__main__":
    diagnose_ecpay_order()
