import importlib.util

# 修改SDK 路徑
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",    # SDK檔名不用改
    "app\\ecpay_payment_sdk.py"    # 結構有變更的話記得改路徑
                                       
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
from datetime import datetime

def main(order_params=None):
	# 修改商品資訊
	order_params = {
        'MerchantTradeNo': datetime.now().strftime("NO%Y%m%d%H%M%S"),
		'StoreID': '',
		'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
		'PaymentType': 'aio',
		'TotalAmount': 150,         
		'TradeDesc': '訂單測試',     
		'ItemName': '尊貴藍勾勾#藍鑽會員',    # 商品名稱，用#當分行
		#'ReturnURL': 'https://www.ecpay.com.tw/return_url.php',  # 後端接收付款結果的 API-綠界的測試API for測試
		'ReturnURL': 'http://localhost:5000/api/payment/result',  # 後端接收付款結果的 API-自製的API for正式 ，需改成外網可訪問的網址
		'ChoosePayment': 'Credit',      
		'ItemURL': 'https://www.ecpay.com.tw/item_url.php',     # 商品資訊頁面(綠界測試用)，需改成外網可訪問的網址
		#'ItemURL': 'http://localhost:3000',  # 前端網址(正式)，需改成外網可訪問的網址
		'Remark': '交易備註',         
		'ChooseSubPayment': '',
        #'ClientBackURL': 'http://localhost:3000/payment/success',  # 前端付款完成頁面，需有「返回商店」功能，需改成外網可訪問的網址
        'OrderResultURL': 'http://localhost:3000/api/payment/result',  # 點擊「返回商店」時跳轉，需改成外網可訪問的網址
        #'OrderResultURL': 'https://www.ecpay.com.tw/order_result_url.php', 
		'NeedExtraPaidInfo': 'Y',
		'DeviceSource': '',
		'IgnorePayment': '',
		'PlatformID': '',
		'InvoiceMark': 'N',
		'CustomField1': '',
        'CustomField2': '',
		'CustomField3': '',
		'CustomField4': '',
		'EncryptType': 1,
    }
		
	extend_params_1 = {
		'ExpireDate': 7,    # 商品上架期限
		'PaymentInfoURL': 'https://www.ecpay.com.tw/payment_info_url.php',  #付款資訊頁面
		'ClientRedirectURL': '',  # 看完付款資訊，要重導到哪裡
	}
		
	extend_params_2 = {
		'StoreExpireDate': 15,
		'Desc_1': '',
		'Desc_2': '',
		'Desc_3': '',
		'Desc_4': '',
		'PaymentInfoURL': 'https://www.ecpay.com.tw/payment_info_url.php',
		'ClientRedirectURL': '',
    }
	
	extend_params_3 = {
        'BindingCard': 0,
		'MerchantMemberID': '',
    }
		
	extend_params_4 = {
		'Redeem': 'N',
		'UnionPay': 0,
    }
	
	# 發票資訊
	inv_params = {
		# 'RelateNumber': 'Tea0001', # 特店自訂編號
		# 'CustomerID': 'TEA_0000001', # 客戶編號
		# 'CustomerIdentifier': '53348111', # 統一編號
		# 'CustomerName': '客戶名稱',
		# 'CustomerAddr': '客戶地址',
		# 'CustomerPhone': '0912345678', # 客戶手機號碼
		# 'CustomerEmail': 'abc@ecpay.com.tw',
		# 'ClearanceMark': '2', # 通關方式
		# 'TaxType': '1', # 課稅類別
		# 'CarruerType': '', # 載具類別
		# 'CarruerNum': '', # 載具編號
		# 'Donation': '1', # 捐贈註記
		# 'LoveCode': '168001', # 捐贈碼
		# 'Print': '1',
		# 'InvoiceItemName': '測試商品1|測試商品2',
		# 'InvoiceItemCount': '2|3',
		# 'InvoiceItemWord': '個|包',
		# 'InvoiceItemPrice': '35|10',
		# 'InvoiceItemTaxType': '1|1',
		# 'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
		# 'DelayDay': '0', # 延遲天數
        # 'InvType': '07', # 字軌類別
	}
		
	# 建立實體
	ecpay_payment_sdk = module.ECPayPaymentSdk(
        # 參考綠界後台->系統開發管理->系統界接設定，開發時有測試用的 商店ID
        MerchantID='3002607',
        
        # 參考綠界後台->系統開發管理->系統界接設定，開發時有測試用的 HashKey
        HashKey='pwFHCqoQZGmho4w6',
        
        # 參考綠界後台->系統開發管理->系統界接設定，開發時有測試用的 HashIV
        HashIV='EkRm7iFT261dpevs'
	)
	
	# 合併延伸參數
	order_params.update(extend_params_1)
	order_params.update(extend_params_2)
	order_params.update(extend_params_3)
	order_params.update(extend_params_4)
		
	# 合併發票參數
	order_params.update(inv_params)
		
	try:
		# 產生綠界訂單所需參數
		order_params = {k: v for k, v in order_params.items() if v != ''}
		final_order_params = ecpay_payment_sdk.create_order(order_params)
		
		# 產生 html 的 form 格式
		action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
		# action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
		html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)

		# 最後產出 html，回傳回去顯示此 html
		return html
	except Exception as error:
		print('An exception happened: ' + str(error))