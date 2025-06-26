# 運行

## 運行 react

```bash
cd frontend

npm run dev
```

### 除錯

- vite@7.0.0 和 react-router-dom@7.6.2 需要 Node.js 版本 >=20。

## 啟動後端伺服器

> 記得 Python 使用正確的 Python 解譯器和環境

```bash
# macOS / Linux
source venv/bin/activate

# Windows（CMD）
venv\Scripts\activate.bat

# Windows（PowerShell）
venv\Scripts\Activate.ps1
```

執行以下指令，確認是否使用正確的 Python 解譯器：

```bash
which python
```

輸出的路徑應該指向你的虛擬環境，例如：

```bash
~/專案資料夾/backend/venv/bin/python
```

啟動開發伺服器以測試環境：

```bash
cd backend

python manage.py runserver
```
