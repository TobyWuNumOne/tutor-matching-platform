# 如何建置專案

## 需求

以下是基於你所提供的資訊，使用 `venv` 方式來啟動專案的建議步驟，並在完成基礎開發環境後，教你如何將環境轉移到 Docker。

1. **前端技術**: React.js (透過 Vite 安裝) + SCSS + Bootstrap
2. **後端技術**: Python + Django
3. **資料庫**: MariaDB
    - 遠端資料庫伺服器：
        - 主機: `fs101.coded2.fun`
        - Port: `3306`
4. **環境管理**: 初期使用 `venv`，後續轉移到 Docker。
5. **版本控制**: Git + GitHub
    - 已創建好儲存庫，並成功複製到本地。
6. **使用 venv 建立開發環境**

---

### **1. 後端環境設置**

#### 創建虛擬環境並安裝依賴

1. 在專案目錄下創建後端目錄：

    ```bash
    mkdir backend && cd backend
    ```

2. 創建 Python 虛擬環境：

    ```bash
    python -m venv venv
    ```

3. 啟用虛擬環境：

    - **Linux/Mac**:

        ```bash
        source venv/bin/activate
        ```

    - **Windows**:

        ```bash
        venv\Scripts\activate
        ```

4. 安裝必要套件：

    ```bash
    pip install django mysqlclient
    ```

    - `mysqlclient`: 用於與 MariaDB 互動的驅動程式。

#### 初始化 Django 專案

1. 初始化 Django 專案並創建應用：

    ```bash
    django-admin startproject backend .
    python manage.py startapp api
    ```

2. 配置 MariaDB 資料庫：
   編輯 `backend/settings.py`，更新資料庫設定：

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '<your-database-name>',  # 資料庫名稱
            'USER': '<your-username>',       # 資料庫使用者名稱
            'PASSWORD': '<your-password>',   # 資料庫密碼
            'HOST': 'fs101.coded2.fun',      # 遠端主機
            'PORT': '3306',                  # 資料庫端口
        }
    }
    ```

3. 執行資料庫遷移：

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

#### 啟動後端伺服器

1. 啟動開發伺服器以測試環境：

    ```bash
    python manage.py runserver
    ```

---

### **2. 前端環境設置**

#### 創建 React 專案

1. 返回專案根目錄，創建前端目錄：

    ```bash
    mkdir ../frontend && cd ../frontend
    ```

2. 使用 Vite 初始化 React 專案：

    ```bash
    npm create vite@latest . -- --template react
    ```

3. 安裝必要套件：

    ```bash
    npm install sass bootstrap axios react-router-dom
    ```

#### 配置 React 應用

1. 在 `src/` 下創建結構化目錄：

    ```zsh
    ├── components/
    ├── pages/
    ├── styles/
    ```

2. 編寫基本的 `App.jsx`，測試前端是否正常運行。

#### 啟動前端開發伺服器

```bash
npm run dev
```

---

### **3. 整合前後端**

1. 在 React 中使用 `axios` 發送 API 請求到 Django 後端。
2. 確保 MariaDB 已正確連接，並測試基本的 CRUD 功能。

---

### **4. 設置 Git 版本控制**

#### 初始化 Git 並提交專案

1. 回到專案根目錄，確認 `.gitignore` 文件內容：

    ```plaintext name=.gitignore
    node_modules/
    venv/
    *.pyc
    __pycache__/
    .env
    ```

2. 提交專案：

    ```bash
    git add .
    git commit -m "初始化專案環境"
    git push origin main
    ```

---

## **將環境轉移到 Docker**

### **1. 創建 Dockerfile**

#### 後端 Dockerfile

```dockerfile name=backend/Dockerfile
# 使用 Python 基礎映像
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 複製需求檔案並安裝依賴
COPY requirements.txt .
RUN pip install -r requirements.txt

# 複製專案
COPY . .

# 開放埠
EXPOSE 8000

# 啟動指令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

#### 前端 Dockerfile

```dockerfile name=frontend/Dockerfile
# 使用 Node.js 基礎映像
FROM node:16

# 設定工作目錄
WORKDIR /app

# 複製 package.json 並安裝依賴
COPY package.json .
RUN npm install

# 複製專案
COPY . .

# 開放埠
EXPOSE 3000

# 啟動指令
CMD ["npm", "run", "dev"]
```

---

### **2. 創建 docker-compose.yml**

使用 `docker-compose` 來管理專案的多容器環境：

```yaml name=docker-compose.yml
version: "3.8"
services:
    backend:
        build:
            context: ./backend
        ports:
            - "8000:8000"
        environment:
            - DB_HOST=fs101.coded2.fun
            - DB_PORT=3306
            - DB_NAME=<your-database-name>
            - DB_USER=<your-username>
            - DB_PASSWORD=<your-password>

    frontend:
        build:
            context: ./frontend
        ports:
            - "3000:3000"

    db:
        image: mariadb:latest
        ports:
            - "3306:3306"
        environment:
            MYSQL_ROOT_PASSWORD: <root-password>
            MYSQL_DATABASE: <your-database-name>
            MYSQL_USER: <your-username>
            MYSQL_PASSWORD: <your-password>
```

---

### **3. 測試 Docker 化**

1. 啟動容器：

    ```bash
    docker-compose up --build
    ```

2. 測試：
    - 前端：`http://localhost:3000`
    - 後端 API：`http://localhost:8000/api`

---

## **結論**

1. **今天的目標**是使用 `venv` 快速建立基礎開發環境，完成前後端連接與基本功能測試。
2. 在基礎功能完成後，依照上述步驟逐步轉移到 Docker，確保團隊協作時的環境一致性，並為最終部署做準備。
3. 如果需要進一步協助，請隨時告訴我！
>>>>>>> fb604415a10bf6f4ce7c966b3ffcb6b84536e235

## 運行 react

```bash
cd frontend

npm run dev
```

### 除錯
-   vite@7.0.0 和 react-router-dom@7.6.2 需要 Node.js 版本 >=20。

## 運行後端伺服器

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
