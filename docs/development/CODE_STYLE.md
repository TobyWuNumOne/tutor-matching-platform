# 🌟 程式碼風格指南 (Code Style Guide)

> 提供一個通用的程式碼風格指南，以幫助維護和閱讀其他人的程式碼。請盡量遵守這些規則，以保持一致性和可讀性。

## 命名規則

- **變數與函數**: 駝峰式命名 (如 `userLogin`)
- **類別與構造器**: 帕斯卡命名法 (如 `UserAuth`)
- **常數**: 全大寫與底線分隔 (如 `MAX_RETRY_COUNT`)

> 不要太亂就好至少知道是幹嘛的

## 排版 🌟🌟

> 避免在版本控制中大量出現排版上的編輯，而不是對於程式碼的撰寫

- 在操作符號（如 =、+）前後加空格。
- **縮排**: 使用 **4 空格**
- **排版**:
  - 使用 [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
  - python 使用 black farmatter

## 檔案結構（待討論）

- 每個檔案只包含一個主要功能
- 將功能模組分成資料夾，如:

```zs
├── backend/         # 後端 Django 應用
│   ├── manage.py
│   ├── backend/     # Django 主目錄
│   ├── api/         # API 模組
├── frontend/        # 前端 React 應用
│   ├── src/
│   ├── package.json
├── docker-compose.yml
├── Dockerfile
├── .env             # 環境變數
├── README.md
└── docs/            # 專案文件
```

## 其他規範

- 每行程式碼不超過 80-100 個字符
- 單引號 (') 或雙引號 ("), 保持一致
- 每個功能模組必須有測試
- 避免過度嵌套。

> 🌟🌟🌟🌟 心有餘力寫個註解，Codereview 也會比較容易
