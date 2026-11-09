# 單字筆記與複習系統 (Vocabulary Note & Review System)

> **一份筆記，產生多張複習卡片 —— 結合 Markdown 單字筆記與 FSRS 間隔重複排程的學習系統**

**組別**：第 13 組  
**組員**：王峻俞、仲若華、曾保齊、葉承昕、關建燊

---

## 📌 專案簡介與動機

傳統單字卡 App 擅長「看題目、想答案」，但學習單字往往需要記錄例句、詞性、出處與個人理解。當筆記與單字卡散落在不同工具時，不僅無法互相連結，還需要重複輸入。

本專案旨在打造**「一份筆記、產生多張複習卡片」**的單字學習系統：
- 每個單字擁有一份專屬 **Markdown 筆記** 與結構化 **屬性欄位**（意思、讀音、出處、詞性等）。
- 從同一份筆記的屬性可自動或手動衍生多張不同考法的 **複習卡片**（例如：看單字回想意思、看單字輸入讀音）。
- 複習進度與記憶狀態掛載於卡片上，**修改筆記不會遺失學習進度**。
- 整合 **Py-FSRS** 間隔重複演算法安排下次複習時間，並支援 **CSV 批次匯入與匯出備份**。

---

## 🛠️ 技術棧與使用套件

| 工具 / 套件 | 類型 | 用途說明 |
| :--- | :---: | :--- |
| **Python 3.10+** | 程式語言 | 撰寫共用邏輯服務層，以及 CLI、GUI 兩種介面 |
| **`sqlite3`** | Python 內建 | 本機資料庫，儲存筆記、屬性、卡片、卡組與複習紀錄（免架設伺服器） |
| **`csv`** | Python 內建 | 批次匯入單字資料、匯出資料備份 |
| **`tkinter`** | Python 內建 | 桌面 GUI 介面（筆記編輯器、Markdown 預覽觸發、卡組管理） |
| **`markdown`** | 第三方套件 | 將 Markdown 筆記本文轉換為 HTML 以供預覽 |
| **`fsrs` (Py-FSRS)** | 第三方套件 | 依據作答評分（1~4 分）計算並更新卡片記憶狀態與下次到期日 |

---

## 🏗️ 系統架構與資料設計

### 三層式架構（兩種介面，一套核心）

```text
┌────────────────────────────────────────────────────────┐
│  介面層 (UI Layer)                                      │
│  ├── CLI 介面：快速新增單字、搜尋、編輯屬性、文字輸入複習   │
│  └── GUI 介面 (Tkinter)：Markdown 筆記編輯預覽、卡組管理 │
├────────────────────────────────────────────────────────┤
│  共用功能服務層 (Service Layer)                          │
│  筆記管理 · 屬性管理 · 卡片生成 · 卡組管理 ·               │
│  挑選到期卡片 · 答案正規化與比對 · CSV 匯入匯出            │
├────────────────────────────────────────────────────────┤
│  資料與演算法層 (Data & Algorithm Layer)                 │
│  SQLite 本機資料庫 ｜ CSV 檔案讀寫 ｜ Py-FSRS 排程引擎    │
└────────────────────────────────────────────────────────┘
```

- **規則只寫一次**：CLI 與 GUI 不直接操作資料庫，統一呼叫「共用功能服務層」。
- **資料互通**：兩種介面共用同一個 SQLite 資料庫檔案。

### 資料關聯設計

- **筆記 (Note)** `1 ── N` **屬性 (Attribute)**（意思、讀音、出處、詞性等）
- **筆記 (Note)** `1 ── N` **卡片 (Card)** `N ── 1` **卡組 (Deck)**
- 每張 **卡片 (Card)** 獨立保存 **FSRS 複習狀態**（穩定度、難度、到期日等）與 **複習紀錄 (Review Log)**。
- 以內部 `ID` 識別筆記與卡片，修改單字名稱或筆記內容不會破壞卡片關聯與複習進度。

---

## 🚀 專案實行步驟（四階段開發計畫）

### 階段一：資料基礎與共用核心（Data & Service Layer）
1. **規劃資料庫 Schema**：設計 `notes`（筆記）、`note_attributes`（結構化屬性）、`decks`（卡組）、`cards`（含 Py-FSRS 狀態欄位）、`review_logs`（複習紀錄）等資料表。
2. **建立 SQLite 存取模組**：封裝 CRUD 操作，確保以內部 ID 維護外鍵關聯。
3. **實作答案比對邏輯**：支援「嚴格比對」與「寬鬆比對」（處理前後空白、全半形轉換、Unicode 正規化）。

### 階段二：CLI 介面與複習流程（CLI & Review Engine）
1. **實作單字與屬性指令**：支援從終端機快速新增筆記、搜尋單字、檢視與修改屬性。
2. **實作複習與作答流程**：
   - 載入指定卡組中已到期（Due）的卡片。
   - 顯示題目 → 使用者回想或輸入答案 → 顯示正確答案與比對結果。
   - 使用者自評記憶程度（`1 忘記` / `2 困難` / `3 記得` / `4 簡單`，答錯時提示選「忘記」）。
3. **串接 Py-FSRS**：將評分結果交由 `fsrs` 計算下次複習時間，並寫回 SQLite。

### 階段三：GUI 介面開發（Tkinter GUI）
1. **筆記編輯器與 Markdown 預覽**：建立 Tkinter 視窗供撰寫長篇 Markdown 筆記，並透過 `markdown` 套件轉為 HTML（第一版優先使用系統瀏覽器開啟預覽）。
2. **卡片與卡組管理畫面**：提供視覺化介面新增/編輯卡組、檢視筆記衍生出的卡片列表與到期狀態。

### 階段四：系統整合與資料交換（Integration & CSV）
1. **CSV 批次匯入與匯出**：實作欄位檢查、編碼處理（UTF-8）與重複資料提示，支援批次建立筆記與卡片。
2. **建立範例資料與測試**：準備日文/英文範例單字卡組，驗證 CLI 與 GUI 交互操作時的資料一致性。

> **第一版（MVP 必做範圍）**：固定屬性（意思、讀音、出處、例句）、一種預設卡片模板、Markdown 編輯與瀏覽器預覽、卡組管理、CLI/GUI 共用資料庫與 FSRS 排程。

---

## 🤝 GitHub 團隊協作指南

> 📄 **完整 Step-by-Step 操作教學（含首次下載、日常 `pull`、存檔 `commit`、上傳 `push`、開分支 `branch` 與合併 `merge` 規定）請直接參閱：[GitHub協作指南.md](./GitHub協作指南.md)**
>
> 🔗 **專案儲存庫網址**：`https://github.com/jackwang941214-art/vocab-review.git`

為了讓 5 位組員能順暢並行開發、避免程式碼衝突與資料庫覆蓋，請遵循以下 Git / GitHub 協作規範：

### 1. 事前準備与 `.gitignore` 設定
- **切勿將個人測試用的 `.db` / `.sqlite3` 檔案或虛擬環境 `.venv/` 提交至 Git**（避免每次複習測試都產生二進位衝突）。
- 請在專案根目錄建立 `.gitignore`，加入：
  ```gitignore
  .venv/
  venv/
  __pycache__/
  *.pyc
  *.db
  *.sqlite3
  .DS_Store
  ```
- 若需提供範例資料，請提交 `seed_data.csv` 或初始化腳本 `init_db.py`。

### 2. 分支策略（GitHub Flow）
- **`main` 分支**：保持隨時可執行的穩定狀態，**禁止直接 `git push` 到 `main`**。
- **功能分支（Feature Branches）**：每位組員開發新功能或修復問題時，都從最新的 `main` 切出新分支：
  - `feat/db-schema`（資料庫與 модели）
  - `feat/fsrs-service`（FSRS 排程與答案比對服務）
  - `feat/cli-interface`（CLI 介面）
  - `feat/gui-editor`（Tkinter GUI 介面）
  - `feat/csv-import-export`（CSV 匯入匯出）
  - `fix/answer-compare-space`（Bug 修復）

### 3. 日常協作標準流程（Step-by-Step）

1. **同步最新主幹**：
   ```bash
   git checkout main
   git pull origin main
   ```
2. **建立並切換至功能分支**：
   ```bash
   git checkout -b feat/你的功能名稱
   ```
3. **分段提交（Commit）**：完成一個小階段就提交，訊息清楚標示類型：
   ```bash
   git add .
   git commit -m "feat(db): 建立 notes 與 cards SQLite 資料表"
   ```
   - 常用前綴：`feat`（新功能）、`fix`（修 Bug）、`docs`（文件）、`refactor`（重構）。
4. **推送分支並發起 Pull Request (PR)**：
   ```bash
   git push -u origin feat/你的功能名稱
   ```
   - 至 GitHub 頁面點擊 **Compare & pull request**。
   - 在 PR 描述中說明本次修改內容與測試方式，並指定 **至少 1 位組員進行 Code Review**。
5. **審查與合併（Merge）**：
   - 確認無衝突且執行正常後，由審查者或負責整合的組員點擊 **Merge pull request**。
   - 合併後可刪除遠端與本地已完成的 feature 分支。

### 4. 介面與服務層分工建議（降低 Merge Conflict）
由於本專案採用「三層式架構」，建議組員以**目錄/模組**切分責任範圍，避免多人同時修改同一個檔案：
- `src/db/`：負責 SQLite 連線、建表與基本資料存取。
- `src/services/`：負責筆記/卡片業務邏輯、FSRS 排程封裝、答案比對、CSV 處理（**先與組員定義好函式名稱與參數回傳格式**）。
- `src/cli/`：負責終端機互動介面（只呼叫 `services`）。
- `src/gui/`：負責 Tkinter 視窗介面（只呼叫 `services`）。

---

## 📚 參考資料
1. [Python `sqlite3` 官方文件](https://docs.python.org/3/library/sqlite3.html)
2. [Python `csv` 官方文件](https://docs.python.org/3/library/csv.html)
3. [Python `tkinter` 官方文件](https://docs.python.org/3/library/tkinter.html)
4. [Py-FSRS 原始碼與使用說明](https://github.com/open-spaced-repetition/py-fsrs)
5. [Py-FSRS API 文件](https://open-spaced-repetition.github.io/py-fsrs/)
6. [FSRS 演算法概念 (The Algorithm)](https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm)
