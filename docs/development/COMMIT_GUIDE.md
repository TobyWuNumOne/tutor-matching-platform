# 💬 Git 提交訊息規範 (Conventional Commits)

## 📋 基本格式

```markdown
<type>(<scope>): <subject>

<body>

<footer>
```

## 🏷️ 提交類型 (Type)

### 主要類型

- feat     - 新功能 (feature)
- fix      - 修復 bug
- docs     - 文件更新
- style    - 代碼格式調整 (不影響功能)
- refactor - 代碼重構 (既不修復 bug 也不新增功能)
- test     - 測試相關
- chore    - 雜務 (構建過程、輔助工具變動)

### 特殊類型

- perf     - 性能優化
- ci       - CI 配置修改
- build    - 構建系統修改
- revert   - 撤銷之前的 commit

## 🎯 範圍 (Scope) - 可選

### 按功能模組

- auth     - 會員系統
- matching - 家教媒合
- rating   - 評價系統
- payment  - 交易系統
- admin    - 後台管理

### 按技術層面

- api      - API 相關
- ui       - 使用者介面
- db       - 資料庫
- config   - 設定檔案

## ✍️ 實際範例

### 簡單提交

```bash
git commit -m "feat: add user login functionality"
git commit -m "fix: resolve password validation error"
git commit -m "docs: update README with setup instructions"
```

### 完整提交

```bash
git commit -m "feat(auth): add user registration with email verification

- Add registration form with validation
- Integrate with email service for verification
- Add password strength requirements
- Include terms of service checkbox

Closes #142"
```

### 不同類型範例

```bash
# 新功能
git commit -m "feat(matching): implement teacher search filters"

# Bug 修復
git commit -m "fix(payment): resolve checkout calculation error"

# 文件更新  
git commit -m "docs(api): add authentication endpoints documentation"

# 代碼重構
git commit -m "refactor(auth): simplify user validation logic"

# 性能優化
git commit -m "perf(matching): optimize search query performance"

# 測試
git commit -m "test(auth): add unit tests for login validation"

# 雜務
git commit -m "chore: update dependencies to latest versions"
```

## 📝 撰寫指導原則

### Subject (標題) 規範

- ✅ 使用現在式動詞 ("add" 不是 "added")
- ✅ 不要大寫開頭
- ✅ 結尾不要句號
- ✅ 50 字元以內
- ✅ 描述「做了什麼」而不是「為什麼做」

### Body (內容) 規範

- 詳細描述「為什麼」和「如何」
- 使用現在式動詞
- 包含重要的技術細節
- 每行不超過 72 字元

### Footer (頁腳) 規範

- Closes #123          - 關閉 Issue
- Fixes #123           - 修復 Issue  
- Refs #123            - 參考 Issue
- Breaking Change:     - 重大變更說明
- Co-authored-by:      - 協作者資訊

## 🚀 實用技巧

### 📋 提交前檢查清單

- [ ] 提交訊息清楚描述變更
- [ ] 使用正確的 type 和 scope
- [ ] 檢查拼寫和語法
- [ ] 確認變更相關的 Issue 編號
- [ ] 單一提交只包含一個邏輯變更

### ⚡ 快速命令

```bash
# 修改最後一次提交訊息
git commit --amend -m "new message"

# 查看提交歷史
git log --oneline -10

# 查看某個檔案的提交歷史
git log --oneline -- filename.js

# 搜尋提交訊息
git log --grep="user login"
```

### 🔧 Git 別名設定

```bash
# 在 ~/.gitconfig 中新增
[alias]
    cm = commit -m
    ca = commit -am
    co = checkout
    st = status -s
    lg = log --oneline --graph --all -10
```

使用範例：

```bash
git cm "feat: add user profile page"
git ca "fix: resolve styling issues"
```

## 🎯 團隊協作規範

### 📅 提交頻率建議

- **小修改**: 隨時提交
- **功能開發**: 每日至少一次
- **重大功能**: 分階段提交
- **Bug 修復**: 立即提交

### 🔄 提交策略

開發中:

- 使用描述性的臨時提交
- 功能完成前可以有多個 WIP commits

PR 前:

- 整理提交歷史 (git rebase -i)
- 合併相關的小提交
- 確保每個提交都有意義

### 📊 提交訊息統計

團隊可以定期檢視：

- 各類型提交的比例
- 提交頻率和品質
- Issue 關閉效率

## ❌ 常見錯誤

### 不好的提交訊息

```bash
❌ git commit -m "fix"
❌ git commit -m "更新程式碼"  
❌ git commit -m "WIP"
❌ git commit -m "Fixed the bug in the login system that was causing issues"
```

### 好的提交訊息

```bash
✅ git commit -m "fix(auth): resolve login validation error"
✅ git commit -m "feat: add user profile editing functionality"  
✅ git commit -m "docs: update API documentation for payment endpoints"
✅ git commit -m "refactor: simplify user authentication logic"
```

## 🆘 常見問題

**Q: 一個提交可以包含多個檔案的修改嗎？**
>A: 可以，但必須是邏輯上相關的變更

**Q: 如何處理重大變更 (Breaking Changes)？**
>A: 在 footer 加上 `BREAKING CHANGE:` 說明

**Q: 提交後發現訊息有錯怎麼辦？**  
>A: 使用 `git commit --amend` 修改 (僅限未推送的提交)

**Q: 可以用中文寫提交訊息嗎？**
>A: 建議使用中文
