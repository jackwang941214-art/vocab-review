# 🤝 第 13 組 GitHub 團隊協作手冊（新手完整圖解版 SOP）

本文件為「**單字筆記與複習系統**」專題的 Git 與 GitHub 標準操作流程。考慮到組內有同學是第一次使用 Git / GitHub，本手冊從**名詞觀念、環境設定、日常寫扣存檔、上傳，到如何合併（Merge）與解衝突**都有詳細一步一步的說明，照著按就能順利完成！

- **專案 GitHub 網址**：https://github.com/jackwang941214-art/vocab-review
- **專案邀請設定網址（組長專用）**：https://github.com/jackwang941214-art/vocab-review/settings/access
- **Clone 下載網址**：`https://github.com/jackwang941214-art/vocab-review.git`

---

## 💡 30 秒搞懂 Git 與 GitHub 在做什麼？（新手必讀）

在開始打指令前，先理解這幾個常見單字的意思，就不會覺得自己在背咒語：

| 名詞 | 白話文解釋 | 對應指令或動作 |
| :--- | :--- | :--- |
| **Repository (Repo)** | **專案資料夾**（GitHub 雲端上放我們整個專題的地方） | 網址 `.../vocab-review` |
| **Clone** | **第一次下載**：把雲端上的整個專案資料夾完整複製一份到自己電腦 | `git clone 網址` |
| **Branch（分支）** | **平行時空 / 個人工作桌**：<br>`main` 是大家共用的「最終成品桌」。為了怕你寫到一半的程式弄壞別人的進度，每個人要寫功能前，都要複製一張自己的「個人工作桌（分支）」來寫。 | `git checkout -b 分支名` |
| **Add & Commit** | **在自己電腦裡存檔（拍快照）**：<br>在 VS Code 按 `Ctrl+S` 只是存在硬碟；`Commit` 則是讓 Git 幫你留下一筆「歷史紀錄點」，寫壞了隨時可以時光倒流。**（此時檔案還在你電腦，隊友還看不到）** | `git add .`<br>`git commit -m "說明"` |
| **Push（推送）** | **上傳到雲端**：把你電腦裡「個人分支」存好的進度，上傳到 GitHub 網站上。 | `git push` |
| **Pull（拉取）** | **從雲端下載更新**：把隊友已經完成、合併進雲端 `main` 的最新檔案，更新到你的電腦裡。 | `git pull origin main` |
| **Pull Request (PR)** | **申請合併審查**：「我的分支寫好並上傳了，請隊友幫我看一下，沒問題的話請幫我併回 `main` 主幹！」 | 在 GitHub 網頁上按按鈕 |
| **Merge（合併）** | **正式合體**：把兩個不同分支的程式碼合在一起（例如：把你的分支合進 `main`，或是把 `main` 的最新進度合進你的分支）。 | 網頁按 `Merge` 按鈕<br>或指令 `git merge` |

```text
【日常協作流程圖】
雲端 main (主幹) ──(1. pull 更新)──> 你的電腦 main ──(2. checkout -b 開分支)──> 你的分支 (feat/xxx)
                                                                                    │
雲端 main <──(5. 網頁按 Merge 合併)── 網頁開 PR 申請 <──(4. push 上傳)── (3. add & commit 存檔)
```

---

## ⚠️ 三大黃金鐵則

1. **禁止直接在 `main` 分支上寫程式或直接 `push` 到 `main`**：寫任何東西前，一定要切到自己的分支（Branch）。
2. **每次動工前，一定要先 `pull` 最新進度**：確保你拿到隊友最新寫好的程式碼。
3. **不要上傳個人的 `.db` / `.sqlite3` 資料庫檔與 `.venv` 資料夾**：`.gitignore` 已經幫大家自動排除，請勿手動強制上傳。

---

## 👑 組長專區：如何發送協作邀請給組員？

組長建立好 GitHub 儲存庫後，其他 4 位組員預設是「路人（唯讀）」，沒有權限上傳程式碼。請組長照以下步驟邀請組員：

1. 先請 4 位組員註冊好 GitHub 帳號，並把他們的 **GitHub 帳號名稱（Username）** 或 **註冊信箱（Email）** 傳到群組。
2. 組長登入 GitHub，直接點擊這個網址進入權限設定頁：  
   👉 [https://github.com/jackwang941214-art/vocab-review/settings/access](https://github.com/jackwang941214-art/vocab-review/settings/access)  
   *(或者從專案首頁上方最右邊點 ⚙️ **`Settings`** → 左側選單點 **`Collaborators`**)*
3. 點擊中間綠色的 **`Add people`** 按鈕。
4. 在搜尋框輸入組員的 **GitHub 帳號** 或 **Email**，點選跳出來的組員頭像。
5. 點擊綠色的 **`Add <組員帳號> to this repository`**。
6. 重複步驟 3~5 把 4 位組員都加進來（此時狀態會顯示 `Pending Invite` 等待接受）。

---

## 零、 組員第一次加入專案（每個人只需做一次！）

### 步驟 1：接受組長的協作邀請（沒按這個會無法上傳！）
組長邀請你之後，你有兩種方式可以接受（二選一）：
- **方法 A（最快）**：登入你的 GitHub 後，直接點開我們的專案網址：[https://github.com/jackwang941214-art/vocab-review](https://github.com/jackwang941214-art/vocab-review)，畫面上方會出現黃色框框，點擊綠色的 **`Accept invitation`** 按鈕。
- **方法 B**：去你的註冊信箱收信，找到標題為 `[GitHub] @jackwang941214-art has invited you to collaborate...` 的信，點進裡面的 **`View invitation`** → **`Accept invitation`**。

### 步驟 2：在電腦設定你的 Git 身分（第一次裝 Git 必做）
如果電腦是第一次使用 Git，沒有設定名字和信箱的話，待會存檔（Commit）時會跳出紅字錯誤 `Author identity unknown`。  
請打開 VS Code，按鍵盤 **`Ctrl + ~`**（在 Esc 下方那顆鍵）打開下方終端機（Terminal），輸入以下兩行（請換成你的名字與信箱）：
```bash
git config --global user.name "你的英文或中文名字"
git config --global user.email "你的GitHub信箱@example.com"
```

### 步驟 3：把專案下載（Clone）到自己電腦
1. 在終端機切換到你想放這個專題的資料夾（例如桌面 `cd Desktop`），然後輸入：
   ```bash
   git clone https://github.com/jackwang941214-art/vocab-review.git
   ```
2. 下載完成後，用 VS Code 打開這個資料夾：
   - 點擊 VS Code 左上角 **`檔案 (File)`** → **`開啟資料夾 (Open Folder)`** → 選擇剛剛下載下來的 **`vocab-review`** 資料夾。

### 步驟 4：建立 Python 虛擬環境並安裝套件
在 VS Code 打開 `vocab-review` 資料夾後，按 **`Ctrl + ~`** 打開終端機，依序複製貼上以下 3 行指令：

**Windows 使用者**：
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
*(💡 如果第二行跳出紅字說「因為這個系統上已停用指令碼執行...」，請先輸入 `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` 按 Enter，再輸入 `Y` 按 Enter，就能順利執行了！)*

**Mac 使用者**：
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 一、 實作前的前置動作（每次要開始寫程式前必做！）

每次打開電腦準備開發新功能，或是上一個任務已經合併完成、要開始下一個任務時，**請務必在 VS Code 終端機依序輸入以下 3 行指令**：

### 步驟 1：切回 `main` 主分支
```bash
git checkout main
```

### 步驟 2：把雲端上隊友最新的進度拉（Pull）下來
```bash
git pull origin main
```

### 步驟 3：建立並切換到你這次任務的專屬分支（Branch）
```bash
git checkout -b 分支名稱
```

#### 📌 分支（Branch）命名規定
格式為 **`類型/功能簡稱`**（全小寫英文，單字間用 `-` 連接）：
- **`feat/`**：開發新功能
  - `git checkout -b feat/db-schema`（建資料庫）
  - `git checkout -b feat/fsrs-service`（寫 FSRS 排程服務）
  - `git checkout -b feat/cli-review`（寫 CLI 複習功能）
  - `git checkout -b feat/gui-editor`（寫 GUI 筆記編輯器）
  - `git checkout -b feat/csv-import`（寫 CSV 匯入匯出）
- **`fix/`**：修復 Bug
  - `git checkout -b fix/answer-space`（修復答案比對空白問題）
- **`docs/`**：修改文件或簡報
  - `git checkout -b docs/update-readme`

#### 🔍 怎麼確認自己現在在哪個分支？
- **看 VS Code 左下角**：最左下角會有一個分支圖示，上面寫的字就是你現在所在的分支（**絕對不能是 `main`！**）。
- **或是在終端機輸入**：`git branch`，前面有 `*` 號且變綠色的，就是你目前所在的分支。

---

## 二、 實作中：如何存檔（Add & Commit）

當你在 VS Code 裡寫好一個小段落（例如：寫完一個函式、建好一張資料表），請先把檔案按 `Ctrl + S` 儲存，接著在終端機做 Git 存檔：

### 步驟 1：檢查自己改了哪些檔案
```bash
git status
```
- 紅字代表你修改或新增、但還沒準備存檔的檔案。
- 這時候也可以順便檢查有沒有不小心動到別人的檔案。

### 步驟 2：將修改的檔案加入暫存區（Stage）
```bash
git add .
```
*(注意 `add` 後面有一個空白加一顆點 `.`，代表把所有修改過的檔案都打包起來)*

### 步驟 3：建立版本紀錄（Commit 存檔）
```bash
git commit -m "類型(模組): 簡短說明這次改了什麼"
```

#### 📌 Commit 訊息格式規定
請在雙引號內清楚標示你改了哪個部分：
- `git commit -m "feat(db): 建立 notes 與 cards SQLite 資料表"`
- `git commit -m "feat(service): 新增答案嚴格與寬鬆比對函式"`
- `git commit -m "feat(cli): 完成單字新增與搜尋指令"`
- `git commit -m "feat(gui): 新增 Tkinter 主視窗與卡組列表"`
- `git commit -m "fix(service): 修正全形空白未被清除的問題"`

---

## 三、 完成階段任務：如何上傳到 GitHub（Push）

當你在自己電腦測試程式跑起來沒問題，而且已經做完上面的 `git add .` 與 `git commit` 後，就可以上傳到 GitHub 雲端：

### 將你的分支推送（Push）到 GitHub
```bash
git push -u origin 你的分支名稱
```
*(例如：`git push -u origin feat/cli-review`)*

> 💡 **小提示**：同一個分支第一次上傳需要打完整的 `git push -u origin 分支名稱`；如果同一個分支之後又繼續修改並 Commit，第二次上傳只需要打短短的 `git push` 即可！

---

## 四、 如何合併程式碼（Merge 完整教學）⭐ 新手最常卡關區

在 GitHub 協作中，「**Merge（合併）**」有兩種常見情境，請依照你的狀況操作：

---

### 情境 A：【最常用】你的功能寫完了，要把你的分支「合併回 `main` 主幹」
> ⚠️ **規定：我們不在自己電腦裡直接 merge 進 `main`，而是統一在「GitHub 網頁上」透過 Pull Request (PR) 來執行 Merge！**

#### 第 1 步：發起 Pull Request (PR 合併申請)
1. 確認你已經執行過 `git push` 把分支上傳了。
2. 打開瀏覽器前往：[https://github.com/jackwang941214-art/vocab-review](https://github.com/jackwang941214-art/vocab-review)
3. 你會在網頁上方看到一個**淡黃色提示框**，寫著 `feat/你的分支名稱 had recent pushes`，直接點擊右邊綠色的 **`Compare & pull request`** 按鈕。
   - *(如果沒看到黃色框：點網頁上方選單的 **`Pull requests`** → 點右邊綠色的 **`New pull request`** → 將左邊設為 `base: main`，右邊選 `compare: 你的分支名稱` → 點 **`Create pull request`**)*
4. **填寫說明**：
   - 在 `Add a title` 寫標題（例如：`完成 CLI 單字複習與評分功能`）。
   - 在下方大框框簡單寫你改了哪些檔案、怎麼測試。
5. **指定隊友審查（Reviewers）**：
   - 看網頁右邊欄位，點開 **`Reviewers`** 的小齒輪 ⚙️，點選 **至少 1 位組員**。
6. 點擊下方綠色的 **`Create pull request`** 按鈕，然後去 LINE / Discord 群組跟大家說：「我開了 PR 囉，請幫我看一下！」

#### 第 2 步：隊友如何審查（Review）與按下 Merge（合併）按鈕？
1. 被點名的隊友（或組長）點開群組傳來的 PR 網址（或去網頁上方 **`Pull requests`** 點進該筆申請）。
2. 點擊中間偏上的 **`Files changed`** 分頁，就能看到這次新增了哪些綠字、刪掉了哪些紅字。
3. 確認沒問題後，點擊網頁右上角綠色的 **`Review changes`** 按鈕：
   - 選擇 **`Approve`**（核准）
   - 點擊綠色的 **`Submit review`**。
4. 回到 **`Conversation`** 分頁，滑到底下，會看到一個綠色勾勾框框寫著：
   `This branch has no conflicts with the base branch`（此分支與主分支沒有衝突）。
5. **執行 Merge（合併）**：
   - 點擊綠色的 **`Merge pull request`** 按鈕。
   - 再點一次 **`Confirm merge`** 確認按鈕。
   - 當畫面變成紫色的 **`Merged`** 圖示，就代表**你的程式碼已經正式合進 `main` 主幹了！🎉**
   - *(旁邊如果出現 `Delete branch` 按鈕，可以順手點一下把雲端用完的舊分支刪掉，保持乾淨)*

#### 第 3 步：Merge 成功後，所有人該做什麼？
1. 按下 Merge 的人在群組喊一聲：「**`feat/xxx` 已經合併進 `main` 囉，大家記得 pull 更新！**」
2. 寫這個分支的同學，下次要寫新功能時，就在終端機輸入：
   ```bash
   git checkout main
   git pull origin main
   git checkout -b 下一個新任務的分支名稱
   ```

---

### 情境 B：你的分支寫到一半，但隊友剛合併了新功能進 `main`，你要怎麼把隊友的新進度「Merge 進你正在寫的分支」？

舉例：你正在 `feat/cli-review` 分支寫 CLI 介面，結果負責寫服務層的隊友說他把 `feat/fsrs-service` 合併進 `main` 了，你需要用到他剛寫好的函式，這時怎麼辦？

請在你的 VS Code 終端機依序輸入以下 4 行：

1. **先把你目前寫到一半的進度存檔（Commit）起來**：
   ```bash
   git add .
   git commit -m "wip: 暫存目前寫到一半的 CLI 進度"
   ```
2. **先去雲端把最新的 `main` 抓下來更新**：
   ```bash
   git fetch origin main
   ```
3. **把雲端最新的 `main` 合併（Merge）進你現在的分支裡**：
   ```bash
   git merge origin/main
   ```
   - 如果沒有跳出 `CONFLICT`（衝突），代表合併成功！你電腦裡現在同時有隊友剛寫好的檔案，也有你寫到一半的檔案，可以繼續寫了！
   - *(如果跳出一個黑底白字的編輯器畫面請你輸入 Merge 訊息，直接按鍵盤 `:wq` 然後按 Enter 就會儲存退出了)*

---

## 五、 發生合併衝突（Merge Conflict）怎麼辦？（手把手解救教學）

### 什麼時候會發生衝突？
- 如果你改 `src/cli/app.py`，隊友改 `src/gui/window.py` → **完全不會衝突**，Git 會自動完美合併。
- 只有當**你跟隊友剛好修改了「同一個檔案的同一行」**，Git 不知道該聽誰的，才會跳出 `Merge conflict` 請你們決定。

### 狀況 1：在 GitHub 網頁開 PR 時顯示 `This branch has conflicts that must be resolved`
無法按綠色的 Merge 按鈕時，你有兩種解法：

#### 解法一：直接在 GitHub 網頁上解衝突（適合簡單衝突）
1. 點擊 PR 下方提示框右邊的 **`Resolve conflicts`** 按鈕。
2. 網頁會打開編輯器，你會看到被標記紅底的地方長這樣：
   ```python
   <<<<<<< feat/你的分支名稱
   print("這是你寫的程式碼")
   =======
   print("這是隊友在 main 裡寫的程式碼")
   >>>>>>> main
   ```
   - `<<<<<<<` 到 `=======` 之間：是**你寫的**。
   - `=======` 到 `>>>>>>>` 之間：是**目前 `main` 上隊友寫的**。
3. **怎麼修改？**
   把 `<<<<<<< ...`、`=======`、`>>>>>>> ...` 這三行標記符號**通通刪掉**，只留下你們討論後決定要保留的正確程式碼（只留你的、只留隊友的、或兩行都留都可以）。
4. 修改完後，點擊網頁右上角的 **`Mark as resolved`** → 再點擊綠色的 **`Commit merge`**。
5. 回到 PR 頁面，就會看到變回綠色勾勾，可以按 **`Merge pull request`** 了！

#### 解法二：在自己電腦的 VS Code 解衝突（最推薦，還有按鈕可以按！）
1. 在 VS Code 確認你在自己的分支上，打開終端機輸入：
   ```bash
   git fetch origin main
   git merge origin/main
   ```
2. 終端機會顯示 `CONFLICT (content): Merge conflict in 某個檔案.py`。
3. 在 VS Code 左側檔案列表點開那個變紅字的檔案，VS Code 會在衝突段落上方貼心地顯示一排小字按鈕：
   - 點 **`Accept Current Change`**：保留你寫的，刪掉隊友的。
   - 點 **`Accept Incoming Change`**：保留隊友寫的，刪掉你寫的。
   - 點 **`Accept Both Changes`**：兩邊寫的都保留下來（最常用，點完再手動微調順序）。
4. 點選按鈕處理完所有衝突，按 `Ctrl + S` 存檔，確認程式跑得動之後，在終端機輸入：
   ```bash
   git add .
   git commit -m "chore: 解決與 main 分支的合併衝突"
   git push
   ```
5. 這時候再去刷一下 GitHub 網頁上的 PR，衝突就自動消失，可以順利按 **`Merge pull request`** 囉！

---

## 六、 常見凸槌急救包（FAQ）

### Q1：糟糕！我忘記開分支，直接在 `main` 上寫了一堆程式碼（還沒 Commit），怎麼辦？
別慌！只要直接打「建立新分支」的指令，你剛剛改的所有內容會自動跟著搬去新分支，`main` 不會壞掉：
```bash
git checkout -b feat/你的新分支名稱
```

### Q2：糟糕！我忘記開分支，而且已經在本地的 `main` 按了 `git commit`（但還沒 push），怎麼辦？
依序輸入這兩行，就能把剛才存的紀錄搬去新分支，並把本地 `main` 恢復原狀：
```bash
git branch feat/你的新分支名稱
git reset --hard origin/main
git checkout feat/你的新分支名稱
```

### Q3：為什麼我們不能把 `.db` 資料庫檔上傳到 GitHub？
因為 SQLite 的 `.db` 檔是「二進位檔案（不是純文字）」。如果 A 同學測試新增了一個單字，B 同學也測試複習了一張卡片，兩個人把 `.db` 上傳時，Git **完全無法合併二進位檔**，也沒辦法用上面的方法選保留哪一行，會導致專案卡死。  
所以我們統一：
- 程式碼裡寫一個「如果電腦裡沒有 `.db` 檔，就自動建表」的初始化函式。
- 測試用的單字資料統一放在 `data/` 資料夾裡的 `.csv` 純文字檔給大家匯入！

---

## 七、 日常指令懶人包（每次寫程式直接複製貼上！）

```bash
# ==========================================
# 1. 【每次開工前必做三部曲】
# ==========================================
git checkout main
git pull origin main
git checkout -b feat/你的功能名稱

# ==========================================
# 2. 【寫完一個段落，在電腦裡存檔】
# ==========================================
git status
git add .
git commit -m "feat(模組): 簡短說明你改了什麼"

# ==========================================
# 3. 【寫完功能，上傳到 GitHub 準備開 PR】
# ==========================================
git push -u origin feat/你的功能名稱
# （去 GitHub 網頁點 Compare & pull request -> 請隊友 Review 並按 Merge）
```
