---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section {
    font-family: "Microsoft JhengHei", "PingFang TC", "Noto Sans CJK TC", sans-serif;
    background: #FFFFFF;
    color: #222222;
    font-size: 30px;
    padding: 50px 64px;
  }
  h1 { color: #1E3A34; font-size: 44px; }
  h2 { color: #1E3A34; font-size: 40px; margin-bottom: 18px; }
  strong { color: #3F8F7A; }
  table { font-size: 26px; width: 100%; display: table; }
  h3 { color: #3F8F7A; font-size: 26px; margin: 10px 0 4px; }
  th { background: #1E3A34; color: #FFFFFF; }
  td { background: #EEF3F0; }
  blockquote { border-left: none; background: #FFF6D6; color: #1E3A34; padding: 12px 20px; border-radius: 10px; }
  code { background: #EEF3F0; color: #1E3A34; }
  pre { background: #1E2422; color: #E8EEEB; border-radius: 12px; font-size: 26px; }
  pre code { background: transparent; color: #E8EEEB; }
  section.lead { background: #1E3A34; color: #FFFFFF; justify-content: center; }
  section.lead h1 { color: #FFFFFF; font-size: 60px; }
  section.lead p { color: #F2B705; font-size: 30px; }
  section.lead strong { color: #CFE3DA; }
  section::after { color: #5A5A5A; font-size: 16px; }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# 單字筆記與複習系統

期中專題提案｜一份筆記，產生多張複習卡片

**第 13 組　組員：王峻俞、仲若華、曾保齊、葉承昕、關建燊**

<!--
大家好，我們是第 13 組。我們期末想做的是「單字筆記與複習系統」，一個把單字筆記和單字卡複習結合在一起的程式。接下來依序介紹動機、方法、架構、實行計畫和參考資料。
-->

---

## 動機：背了單字，卻沒地方放它的「故事」

單字卡 App 擅長「看題目、想答案」，但學一個單字往往不只是記住一個翻譯。

| 痛點 | 說明 |
|---|---|
| ① 只記翻譯 | 例句、詞性、出處、自己的理解，在單字卡裡沒有地方放 |
| ② 知識散落 | 筆記寫在一個地方、單字卡在另一個 App，兩邊無法互相連結 |
| ③ 重複輸入 | 同一個單字要在筆記和卡片裡各打一次，費時又容易不一致 |

<!--
先說動機。大家都用過單字卡 App，它很擅長「看題目、想答案」，但學單字往往不只記一個翻譯：例句、詞性、出處、自己的理解都沒地方放。結果筆記在一個地方、單字卡在另一個 App，兩邊沒有連結，同一個字還要打兩次。
-->

---

## 目的：一份筆記，產生多張卡片

| 筆記「勉強」 | → | 產生的卡片 |
|---|:-:|---|
| **意思**：學習、用功<br>**讀音**：べんきょう<br>**出處**：日文課 第 3 課<br>例句（Markdown 本文）：毎日日本語を勉強します。 | → | **卡片 A**：勉強 → 回想意思<br><br>**卡片 B**：勉強 → 輸入讀音（嚴格比對） |

- **FSRS** 依作答結果安排下次複習
- **CSV** 匯入匯出，方便建立與備份

<!--
所以我們讓每個單字都有一份自己的筆記：本文用 Markdown 自由整理，意思、讀音、出處另外存成屬性。接著從同一份筆記產生多張卡片，例如「勉強」可以一張考意思、一張考輸入讀音。複習時間交給 FSRS 演算法安排，也支援 CSV 匯入匯出。
-->

---

## 方法：五步驟從筆記到複習

| 步驟 | 做什麼 |
|---|---|
| 1 新增筆記 | 單字當標題，用 Markdown 寫例句與重點 |
| 2 填寫屬性 | 意思、讀音、出處、詞性等結構化欄位 |
| 3 建立卡片 | 選欄位當題目與答案，設定作答與比對方式 |
| 4 編入卡組 | 依目標分組，例如 Unit 1、醫學英文 |
| 5 複習排程 | 作答後評分，FSRS 算出下次複習時間 |

> **素材**：使用者自行輸入的筆記本文、單字屬性、標籤與複習評分紀錄；也能用 CSV 批次匯入。

<!--
使用方法分五步：新增筆記、填寫屬性、從欄位建立卡片並設定作答方式、把卡片編入卡組，最後開始複習。程式會挑出到期的卡片，作答評分後由 FSRS 算出下次複習時間。素材就是使用者自己輸入的筆記和複習紀錄，也能用 CSV 一次匯入。
-->

---

## 使用的工具與套件

| 套件 | 類型 | 用途 |
|---|---|---|
| `Python` | 語言 | 撰寫共用邏輯與 CLI、GUI 兩種介面 |
| `sqlite3` | 內建 | 本機保存筆記、卡片、卡組與紀錄，免架伺服器 |
| `csv` | 內建 | 批次匯入單字資料、匯出備份 |
| `tkinter` | 內建 | 筆記編輯器、Markdown 預覽與卡組管理畫面 |
| `markdown` | 第三方 | 把筆記本文轉成 HTML 以供預覽 |
| `fsrs`（Py-FSRS） | 第三方 | 依評分更新卡片狀態與到期日 |

<!--
工具以 Python 為主。sqlite3、csv、Tkinter 都是 Python 內建，分別負責本機資料庫、CSV 讀寫和桌面視窗；另外用 markdown 套件把筆記轉成 HTML 預覽，用 Py-FSRS 處理間隔複習排程，不用自己推導演算法。
-->

---

## 程式架構：兩種介面，一套核心

| 層 | 內容 |
|---|---|
| **介面層** | CLI：快速新增、編輯屬性、複習 ｜ GUI：Markdown 編輯預覽、卡組管理 |
| ↓ **共用功能服務** | 筆記 · 屬性 · 卡片 · 卡組 · 挑選到期卡片 · 答案比對 · CSV |
| ↓ **資料層** | SQLite ｜ CSV 檔案 ｜ Py-FSRS |

- **規則只寫一次**：CLI 和 GUI 不各自處理資料
- **資料互通**：共用同一個 SQLite 檔

<!--
架構分三層。最上面有兩種介面：CLI 適合快速新增單字和複習，GUI 適合寫長筆記、預覽 Markdown 和管理卡組。兩者都呼叫同一層共用功能服務，最底層的資料層負責 SQLite、CSV 和 FSRS。這樣規則只寫一次，兩邊的資料也一致。
-->

---

## 資料設計：學習進度和筆記分開存

> **屬性** ←一對多— **筆記** —一對多→ **卡片** —編入→ **卡組**
> 每張**卡片**各自帶有：**複習狀態**（記憶狀態、到期日）與**複習紀錄**（作答時間、評分）

- 一份筆記可產生多張卡片
- 複習狀態掛在卡片上，**修改筆記不會遺失學習進度**
- 以內部 ID 識別筆記，改名也不會斷

<!--
資料設計上，一份筆記有多個屬性、可以產生多張卡片，卡片再編入卡組。最重要的是，每張卡片的複習狀態和紀錄跟筆記分開保存，所以修改筆記內容時不會弄丟學習進度。
-->

---

## 複習流程：比對答案，再交給 FSRS

載入到期卡片 → 顯示題目 → 回想或在 CLI 輸入答案 →
顯示答案並比對 → 使用者評分 1–4 → **FSRS 更新排程並儲存**

```text
請輸入這個日文單字的讀音：勉強
你的答案：べんきょう
比對結果：符合 ✓
FSRS 評分：1 忘記／2 困難／3 記得／4 簡單
```

> **答對 ≠ 記得牢**：比對後仍由使用者評分；答錯時提示選「忘記」。

<!--
複習時，程式載入到期卡片、顯示題目，使用者回想或直接在 CLI 輸入答案。像這個例子，輸入「勉強」的讀音後比對結果是符合。但答對不代表記得很牢，所以仍讓使用者在四個等級中評分，答錯就提示選「忘記」。評分交給 Py-FSRS 更新排程，再存回資料庫。
-->

---

## 實行計畫：先打底，再接介面

| 階段 | 內容 |
|---|---|
| ① 資料基礎 | 規劃欄位、建立 SQLite 資料表 |
| ② CLI | 新增、搜尋、編輯屬性；複習與答案比對 |
| ③ GUI | Markdown 編輯與預覽；卡片與卡組管理 |
| ④ 整合 | 串接 FSRS、CSV 匯入匯出、範例資料 |

- **第一版（必做）**：固定屬性（意思、讀音、出處、例句）、一種卡片模板、Markdown 編輯預覽、卡組管理
- **未來擴充**：帳號與網路同步、附件、假名寬鬆比對、依個人紀錄調整 FSRS 參數

<!--
實行計畫分四階段：先建資料庫，再完成 CLI，接著做 GUI 的筆記編輯和卡組管理，最後整合 FSRS 和 CSV。為了控制工作量，第一版只支援固定幾種屬性和一種卡片模板，帳號同步、附件等列為未來擴充。
-->

---

<style scoped>table { font-size: 22px; }</style>

## 可能遇到的困難與對策

| 困難 | 問題 | 對策 |
|---|---|---|
| FSRS 狀態保存 | 排程需要完整卡片狀態，不只到期日 | 依 Py-FSRS API 設計欄位，固定套件版本 |
| 答案比對 | 空白、全半形、Unicode 造成誤判 | 卡片可選嚴格／寬鬆，只做明確的正規化 |
| 答對 ≠ 記得牢 | 比對結果不等於回想難度 | 比對後仍讓使用者評分，答錯建議「忘記」 |
| 介面一致性 | CLI、GUI 各自處理資料易不同步 | 共用服務層與同一資料庫，依序操作 |
| Markdown 預覽 | 內嵌 HTML 元件安裝較麻煩 | 先用系統瀏覽器預覽，再評估內嵌 |
| CSV 與重複資料 | 編碼、分隔符號不同；單字重複匯入 | 檢查欄位並提示錯誤，以內部 ID 識別 |

<!--
預期的困難有幾個。第一，FSRS 需要保存完整的卡片狀態，不只是到期日，我們會依套件 API 設計欄位並固定版本。第二，答案比對容易因為空白、全半形或 Unicode 誤判，所以讓每張卡片選擇嚴格或寬鬆比對。另外還有兩種介面的一致性、Markdown 預覽方式，以及 CSV 格式和重複單字的問題，對策都列在投影片上。
-->

---

## 參考資料

1. Python Software Foundation. [sqlite3 — DB-API 2.0 interface for SQLite databases](https://docs.python.org/3/library/sqlite3.html)
2. Python Software Foundation. [csv — CSV File Reading and Writing](https://docs.python.org/3/library/csv.html)
3. Python Software Foundation. [tkinter — Python interface to Tcl/Tk](https://docs.python.org/3/library/tkinter.html)
4. Open Spaced Repetition. [Py-FSRS（原始碼與使用說明）](https://github.com/open-spaced-repetition/py-fsrs)
5. Open Spaced Repetition. [Py-FSRS API 文件](https://open-spaced-repetition.github.io/py-fsrs/)
6. Open Spaced Repetition. [The Algorithm（FSRS 演算法概念）](https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm)

<!--
最後是參考資料，主要是 Python 官方文件，以及 Open Spaced Repetition 的 Py-FSRS 文件和演算法說明。
-->

---

<!-- _class: lead -->
<!-- _paginate: false -->

# 謝謝聆聽

一份筆記，記住整個單字

**Q & A**

<!--
以上是我們的提案：一份筆記，記住整個單字。謝謝大家。
-->
