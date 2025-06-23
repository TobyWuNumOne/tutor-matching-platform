# 📊 GitHub Projects 使用指南

## 🎯 專案連結

[家教媒合平台開發 Project](https://github.com/users/TobyWuNumOne/projects/4)

## 🖥️ 介面操作

### 📋 Board View (看板視圖)

**用途**: 日常任務管理、快速檢視進度

**操作方式**:

- **移動任務**: 直接拖拉卡片到不同欄位
- **新增任務**: 點擊欄位底部的 "+" 號
- **編輯任務**: 點擊卡片開啟詳細資訊
- **篩選任務**: 使用上方的 Filter 功能

### 📊 Table View (表格視圖)  

**用途**: 批量編輯、詳細資料檢視、數據分析

**切換方式**: 點擊左上角的視圖名稱選擇 "Table"

**進階功能**:

- **排序**: 點擊欄位標題排序
- **群組**: 依照 Assignee、Priority、Feature Area 分組
- **批量編輯**: 選取多個項目同時編輯

## 🔧 自訂欄位使用

### 設定任務屬性

```markdown
Assignee: @TobyWuNumOne / @user1 / @user2
Priority: 🔴 High / 🟡 Medium / 🟢 Low
Feature Area: 選擇對應的功能模組
Story Points: 1, 2, 3, 5, 8, 13
Sprint: 選擇對應的開發週期
Due Date: 設定預期完成日期
```

### 批量設定技巧

1. 切換到 Table View
2. 選取多個相同類型的任務
3. 統一設定 Feature Area 或 Priority

## 🔍 篩選與搜尋

### 常用篩選器

```bash
# 顯示指派給自己的任務
assignee:@me

# 顯示高優先級任務  
priority:"🔴 High"

# 顯示特定功能模組
"feature area":"🔐 會員系統"

# 顯示進行中的任務
status:"🔄 In Progress"

# 組合篩選
assignee:@me status:"🔄 In Progress"
```

### 搜尋技巧

- **關鍵字搜尋**: 在搜尋框輸入任務名稱關鍵字
- **標籤搜尋**: `label:frontend` 顯示前端相關任務
- **狀態搜尋**: `is:open` 顯示未完成任務

## 🤖 自動化功能

### 已設定的自動化

- ✅ **新 Issue** → 自動加入 Project Backlog
- ✅ **Issue 指派** → 自動移到 Ready
- ✅ **PR 開啟** → 自動移到 Code Review  
- ✅ **Issue/PR 關閉** → 自動移到 Done
- ✅ **部署成功** → 自動移到 Deployed

### 手動觸發自動化

- **移動任務**: 拖拉到對應欄位會觸發相關動作
- **設定 Assignee**: 會自動更新任務狀態
- **關閉 Issue**: 會自動完成對應任務

## 📈 進度追蹤

### 個人儀表板

```markdown
我的任務篩選: assignee:@me
今日任務: assignee:@me status:"🔄 In Progress"  
本週完成: assignee:@me status:"✅ Done" updated:>2025-06-17
```

### 團隊概況

- **Table View** → 依 Assignee 群組 → 查看每人工作負荷
- **篩選 High Priority** → 檢視緊急任務處理狀況
- **依 Feature Area 群組** → 查看各模組開發進度

## 💡 使用技巧

### 📅 日常檢查清單

```markdown
每天早上 (5 分鐘):
1. 檢視自己的 "In Progress" 任務
2. 確認今日優先處理項目
3. 查看是否有 Code Review 請求

每天晚上 (3 分鐘):  
1. 更新任務進度
2. 移動完成的任務
3. 規劃明日工作
```

### 🎯 週期性檢視

```markdown
每週一 Sprint Planning:
1. 檢視上週完成項目
2. 從 Backlog 選擇本週任務
3. 設定 Story Points 和優先級
4. 分配給團隊成員

每週五 Sprint Review:
1. 統計完成的 Story Points
2. 檢討未完成的任務
3. 調整下週優先級
```

### ⚡ 快捷操作

- **快速新增**: 在任何欄位底部直接輸入任務標題
- **快速編輯**: 雙擊卡片標題直接編輯
- **批次移動**: 選取多個任務一次移動
- **複製任務**: 點擊任務 → "..." → "Convert to issue"

## 🆘 疑難排解

**Q: 任務沒有自動加入 Project？**
>A: 檢查 Issue 是否有正確的 repository，手動加入 Project

**Q: 拖拉卡片沒有反應？**  
>A: 重新整理頁面，確認網路連線正常

**Q: 看不到某些欄位？**
>A: 檢查篩選器設定，或切換到 Table View 查看完整資訊

**Q: 如何恢復誤刪的任務？**
>A: 到對應的 Issue 頁面重新加入 Project
