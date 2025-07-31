# NotifyURL 實作說明

## 🆕 新增功能

### 1. NotifyURL 路由 (`/api/payment/notify`)

新增了用於接收綠界非同步付款通知的端點，提供比 ReturnURL 更可靠的付款確認機制。

#### 路由詳細資訊
- **URL**: `/api/payment/notify`
- **Method**: `POST`
- **用途**: 接收綠界的非同步付款通知 (NotifyURL)
- **回傳**: `1|OK` (成功) 或 `0|錯誤訊息` (失敗)

#### 主要特色
- ✅ **可靠性**: 綠界會重複發送直到收到確認回應
- ✅ **完整驗證**: 包含 CheckMacValue 驗證
- ✅ **詳細日誌**: 記錄所有通知資料和處理過程
- ✅ **自動啟用**: 付款成功後自動啟用老師藍勾勾認證
- ✅ **錯誤處理**: 完善的異常處理和錯誤回傳

### 2. 更新綠界參數設定

在 `convert_to_ecpay_params()` 函數中新增了 NotifyURL 參數：

```python
'ReturnURL': 'http://localhost:5000/api/payment/result',  # 同步回傳
'NotifyURL': 'http://localhost:5000/api/payment/notify',  # 非同步通知
```

### 3. Swagger 文檔

為 `/notify` 端點新增了完整的 Swagger 文檔，包含：
- 詳細的參數說明
- 回傳格式說明
- 錯誤碼定義
- 使用範例

### 4. 測試頁面更新

更新了 `/api/payment/test` 測試頁面，新增：
- NotifyURL 端點說明
- ReturnURL vs NotifyURL 的差異說明
- 更詳細的付款流程說明

## 🔄 NotifyURL vs ReturnURL 差異

| 項目 | ReturnURL (同步回傳) | NotifyURL (非同步通知) |
|------|---------------------|----------------------|
| **觸發時機** | 付款完成後立即跳轉 | 付款完成後主動發送 |
| **可靠性** | 可能因網路問題失敗 | 重複發送直到確認 |
| **用途** | 用戶體驗和頁面跳轉 | 業務邏輯處理 |
| **回傳格式** | 可以是 HTML 頁面 | 必須回傳 "1\|OK" |
| **重試機制** | 無 | 自動重試 |

## 📋 完整付款流程

1. **建立訂單** → `/api/payment/ecpay` (POST)
2. **跳轉付款** → 綠界付款頁面
3. **同步回傳** → `/api/payment/result` (ReturnURL)
4. **非同步通知** → `/api/payment/notify` (NotifyURL) ⭐ **新增**
5. **啟用認證** → 自動啟用藍勾勾認證
6. **查詢狀態** → `/api/payment/status/<trade_no>`

## 🛠️ 實作重點

### 驗證機制
- CheckMacValue 驗證確保資料完整性
- 必要欄位檢查防止惡意請求
- 訂單存在性驗證

### 業務邏輯
- 付款成功後自動啟用 `teacher.blue_premium = True`
- 更新 Payment 記錄狀態和相關資訊
- 完整的交易記錄追蹤

### 錯誤處理
- 缺少必要欄位 → 回傳 `0|缺少必要欄位`
- 訂單不存在 → 回傳 `0|訂單不存在`
- 系統錯誤 → 回傳 `0|處理錯誤`

## 🚀 使用方式

### 測試 NotifyURL
1. 前往 `http://localhost:5000/api/payment/test`
2. 填寫測試表單建立訂單
3. 完成綠界付款流程
4. 系統會同時接收 ReturnURL 和 NotifyURL 通知

### 查看通知日誌
NotifyURL 會詳細記錄所有處理過程，可以在後端控制台查看：
```
=== 🔔 收到藍勾勾認證付款非同步通知 (NotifyURL) ===
📥 非同步通知資料: {...}
📋 非同步通知詳細資料:
   商店訂單號: BLUE_1_20250729123456
   綠界交易號: 2000132...
   ...
```

## 📚 相關檔案

- **主要實作**: `app/routes/payment_routes.py`
- **模型定義**: `app/models/payment.py`
- **測試頁面**: `/api/payment/test`
- **API 文檔**: `/docs/` (Swagger UI)

## 🔧 生產環境設定

記得在生產環境中更新以下 URL：
```python
'ReturnURL': 'https://yourdomain.com/api/payment/result',
'NotifyURL': 'https://yourdomain.com/api/payment/notify',
```
