# 🔄 開發流程指南

>簡單來說就是根據功能從dev.開分支進行開發，完成功能後刪除分支。

## 🌿 分支策略

Squash and merge（推薦）：
適用於功能分支

- 保持 main 分支歷史簡潔
- 合併時會壓縮所有提交

Merge commit：

- 保留完整的提交歷史
- 適用於重要的里程碑

Rebase and merge：

- 線性的提交歷史
- 需要乾淨的提交紀錄

```markdown
main          (正式環境 - 受保護)
├── develop   (開發環境)
|   ├── feature/user-login    (功能分支)
|   └── feature/course-search (功能分支)
└── hotfix/urgent-fix     (緊急修復)
```

## 📋 標準工作流程

### 1. 接受任務

- 前往 [GitHub Projects](https://github.com/users/TobyWuNumOne/projects/4)
- 選擇 `🎯 Ready` 欄位中的任務
- 點擊任務 → 設定 **Assignee** 為自己
- 移動任務到 `🔄 In Progress`

### 2. 建立功能分支

```bash
# 更新本地 dev 分支
git checkout dev.
git pull origin dev.

# 建立新分支 (命名規範見下方)
git checkout -b feature/user-authentication
```

### 3. 開發功能

- 撰寫代碼
- 撰寫測試
- 本地測試通過

### 4. 提交變更

```bash
# 檢查變更
git status
git diff

# 暫存變更
git add .

# 提交 (遵循 Conventional Commits)
git commit -m "feat(auth): add user login functionality

- Add login form validation
- Integrate with backend API
- Add error handling for invalid credentials
- Add remember me functionality

Closes #123"
```

### 5. 推送並建立 PR

#### PR 檢查清單

```maarkdown
建立 PR 前：

 功能開發完成
 所有測試通過
 程式碼已自我審查
 相關文件已更新
 提交訊息符合規範

建立 PR 時：

 填寫完整的 PR 描述
 連結相關 Issue
 添加適當的標籤
 指定審查者
 提供測試指引
```

```bash
# 1. 從最新的 main 分支建立功能分支
git checkout main
git pull origin main
git checkout -b feature/user-profile-page

# 2. 開發並提交變更
git add .
git commit -m "feat(profile): add user profile editing functionality"

# 3. 推送分支
git push origin feature/user-profile-page

# 4. 到 GitHub 建立 PR
```

### 6. Code Review

- 等待至少 1 人 review
- 根據 feedback 修改
- 所有檢查通過後合併

```markdown
程式碼品質：

 程式碼邏輯正確
 遵循專案編碼規範
 適當的錯誤處理
 沒有明顯的性能問題
 安全性考量

測試與文件：

 測試覆蓋率足夠
 測試案例合理
 相關文件已更新
 API 文件準確

設計與架構：

 符合整體架構設計
 模組化程度適當
 可維護性良好
 遵循 DRY 原則
```

### 7. 清理分支

```bash
# 合併後刪除本地分支
git checkout main
git pull origin main
git branch -d feature/user-authentication
```

## 🏷️ 分支命名規範

```markdown
feature/功能名稱     - 新功能開發
bugfix/問題描述      - Bug 修復
hotfix/緊急修復      - 緊急修復
refactor/重構內容    - 代碼重構
docs/文件更新        - 文件更新
```

**範例**:

- `feature/user-registration`
- `bugfix/login-validation-error`
- `hotfix/payment-gateway-issue`

## ⚡ 開發技巧

### 快速命令

```bash
# 查看目前分支狀態
git status -s

# 查看分支圖
git log --oneline --graph --all -10

# 快速提交 (小修改)
git add . && git commit -m "fix: minor typo correction"

# 查看遠端分支
git branch -r
```

### 常見問題解決

```bash
# 忘記建立分支就開始開發
git stash                    # 暫存變更
git checkout -b feature/xxx  # 建立分支
git stash pop               # 恢復變更

# 需要更新分支到最新版本
git checkout feature/xxx
git rebase main             # 或使用 merge

# 取消最後一次 commit (未推送)
git reset --soft HEAD~1
```

## 🆘 常見問題

Q: PR 被拒絕後怎麼辦？
>A: 根據審查意見修改，推送新的提交，PR 會自動更新

Q: 可以在 PR 中推送新的提交嗎？
>A: 可以，新提交會自動加入到現有的 PR 中

Q: 如何處理合併衝突？

```bash
# 更新本地 main 分支
git checkout main
git pull origin main

# 切換到功能分支並合併 main
git checkout feature/your-branch
git merge main

# 解決衝突後提交
git add .
git commit -m "resolve merge conflicts"
git push origin feature/your-branch
```

Q: PR 太大怎麼辦？
>A: 考慮拆分成多個小的 PR，每個 PR 專注於單一功能
