# 單字筆記與複習系統 (Vocabulary Note & Review System) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立一套結合「Markdown 單字筆記 + 結構化屬性 + 一筆記多卡片衍生 + Py-FSRS 間隔重複排程 + CSV 匯入匯出」的學習系統，並同時提供 CLI 與 Tkinter GUI 兩種介面共用同一套服務層與 SQLite 資料庫。

**Architecture:** 採用三層式架構（UI Layer → Service Layer → Data & Algorithm Layer）。UI 層（`src/cli/`、`src/gui/`）不直接存取資料庫，統一呼叫共用服務層（`src/services/`）；資料層（`src/db/`）以內部 `ID` 維護筆記、屬性、卡組、卡片與複習紀錄的關聯，使修改單字或筆記內容時不會遺失卡片的 FSRS 學習進度。

**Tech Stack:** Python 3.11+、`sqlite3`（內建）、`csv`（內建）、`tkinter`（內建）、`argparse`（內建）、`fsrs==4.1.1`（Py-FSRS）、`markdown==3.7`、`pytest`（測試）。

**Spec:** [README.md](../../../README.md) & [單字筆記與複習系統_期中提案_marp.md](../../../單字筆記與複習系統_期中提案_marp.md)

## Global Constraints

- Python 版本需為 3.10+（目前環境為 Python 3.11.7）。
- 固定第三方套件版本：`fsrs==4.1.1`、`markdown==3.7`（見 `requirements.txt`）。
- 嚴格遵守三層式架構：CLI 與 GUI 僅能呼叫 `src/services/`，不得直接執行 SQL 或操作 `sqlite3`。
- 複習狀態（FSRS `Card` JSON 與 `due_at`）與複習紀錄（`review_logs`）掛載於 `cards` 上，並以內部整數 `note_id` 關聯 `notes`，修改單字名稱或筆記本文不得遺失學習進度。
- MVP 固定屬性鍵值：`meaning`（意思）、`reading`（讀音）、`source`（出處）、`example`（例句）。
- 切勿將 `.db` / `.sqlite3` 或 `.venv/` 提交至 Git（已設定於 `.gitignore`）。
- 每次完成一個 Task 皆須執行對應的 `pytest` 驗證通過後再進行 `git commit`。

---

## 整體專案檔案結構總覽 (File Map)

```text
期末專題/
├── main.py                              # 程式進入點 (--cli 啟動 CLI，預設啟動 GUI)
├── requirements.txt                     # 第三方依賴 (fsrs==4.1.1, markdown==3.7)
├── data/
│   ├── .gitkeep
│   └── seed_data.csv                    # 範例單字資料 (日文/英文)
├── docs/superpowers/plans/
│   └── 2026-11-16-vocab-review-system.md
├── src/
│   ├── __init__.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── connection.py                # SQLite 連線管理、外鍵啟用與建表 (Schema)
│   │   └── repositories.py              # 資料表 CRUD 封裝 (Note, Deck, Card, ReviewLog)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── answer_matcher.py            # 答案正規化與嚴格/寬鬆比對邏輯
│   │   ├── note_service.py              # 筆記與結構化屬性管理服務
│   │   ├── deck_card_service.py         # 卡組管理與「一筆記多卡片」生成服務
│   │   ├── review_service.py            # 到期卡片挑選與 Py-FSRS 排程更新服務
│   │   ├── markdown_service.py          # Markdown 轉 HTML 與系統瀏覽器預覽
│   │   └── csv_service.py               # CSV 批次匯入（含重複檢查）與匯出備份
│   ├── cli/
│   │   ├── __init__.py
│   │   └── app.py                       # argparse 命令列介面與互動式複習流程
│   └── gui/
│       ├── __init__.py
│       └── app.py                       # Tkinter 桌面介面（筆記編輯、預覽、卡組與複習）
└── tests/
    ├── test_db.py
    ├── test_answer_matcher.py
    ├── test_note_service.py
    ├── test_deck_card_service.py
    ├── test_review_service.py
    ├── test_markdown_service.py
    ├── test_csv_service.py
    └── test_cli.py
```

---

## 開發流程與團隊分工建議

| 階段 | 對應 Task | 建議負責分支 (`feat/*`) | 核心產出 |
| :--- | :--- | :--- | :--- |
| **階段一：資料基礎與共用核心** | Task 1 ~ Task 5 | `feat/db-schema`、`feat/fsrs-service` | 環境建置、SQLite Schema、Repositories、答案比對、筆記/卡組/卡片服務 |
| **階段二：複習引擎與 CLI** | Task 6、Task 9 | `feat/fsrs-service`、`feat/cli-interface` | Py-FSRS 排程整合、CLI 指令與終端機互動複習 |
| **階段三：Markdown 預覽與 GUI** | Task 7、Task 10 | `feat/gui-editor` | Markdown 轉 HTML 預覽、Tkinter 筆記/卡組/複習視窗 |
| **階段四：CSV 整合與範例測試** | Task 8、Task 11 | `feat/csv-import-export` | CSV 匯入匯出、`main.py` 整合、`seed_data.csv` 與端對端驗證 |

---

## 階段一：資料基礎與共用核心 (Data & Service Layer)

### Task 1: 開發環境設定與測試框架驗證

**Files:**
- Modify: `requirements.txt` (確認測試工具註記或維持純執行依賴，並於 `.venv` 安裝 `pytest`)
- Create: `tests/__init__.py`

**Interfaces:**
- Produces: 可運作的 `.venv` 虛擬環境，內含 `fsrs==4.1.1`、`markdown==3.7`、`pytest`。

- [ ] **Step 1: 建立並啟用虛擬環境、安裝依賴套件**

Run (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pytest
```
Expected: 安裝完成無錯誤，`pip list` 顯示 `fsrs 4.1.1`、`markdown 3.7`、`pytest`。

- [ ] **Step 2: 驗證 Py-FSRS 4.1.1 API 可用性**

Run:
```powershell
.\.venv\Scripts\python.exe -c "from fsrs import Scheduler, Card, Rating, ReviewLog; s=Scheduler(); c=Card(); c2, log=s.review_card(c, Rating.Good); print(type(c2.to_dict()), type(log.to_dict()))"
```
Expected: `<class 'dict'> <class 'dict'>`

- [ ] **Step 3: 建立 `tests/__init__.py` 並確認 `pytest` 可執行**

```python
"""單字筆記與複習系統測試套件。"""
```

Run: `.\.venv\Scripts\pytest.exe`
Expected: `no tests ran` (exit code 5，代表 pytest 正常運作)。

---

### Task 2: SQLite 資料庫連線與 Schema 建立 (`src/db/connection.py`)

**Files:**
- Create: `src/db/connection.py`
- Test: `tests/test_db.py`

**Interfaces:**
- Produces:
  - `DEFAULT_DB_PATH: Path`
  - `get_connection(db_path: str | Path = DEFAULT_DB_PATH) -> sqlite3.Connection`
  - `init_db(db_path: str | Path = DEFAULT_DB_PATH) -> None`

- [ ] **Step 1: 撰寫失敗測試 `tests/test_db.py` 驗證資料表與外鍵約束**

```python
"""測試 SQLite 資料庫連線與 Schema 初始化。"""

import sqlite3
from pathlib import Path

from src.db.connection import get_connection, init_db


def test_init_db_creates_all_tables(tmp_path: Path) -> None:
    db_file = tmp_path / "test_vocab.db"
    init_db(db_file)

    with get_connection(db_file) as conn:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
        table_names = {row["name"] for row in rows}

    assert {"notes", "note_attributes", "decks", "cards", "review_logs"}.issubset(table_names)


def test_foreign_keys_are_enabled(tmp_path: Path) -> None:
    db_file = tmp_path / "test_fk.db"
    init_db(db_file)

    with get_connection(db_file) as conn:
        fk_status = conn.execute("PRAGMA foreign_keys").fetchone()[0]
        assert fk_status == 1

        try:
            conn.execute(
                "INSERT INTO note_attributes (note_id, attr_key, attr_value) VALUES (?, ?, ?)",
                (999, "meaning", "不存在的筆記"),
            )
            assert False, "應觸發外鍵約束錯誤"
        except sqlite3.IntegrityError:
            pass
```

- [ ] **Step 2: 執行測試確認失敗**

Run: `.\.venv\Scripts\pytest.exe tests/test_db.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'src.db.connection'`

- [ ] **Step 3: 實作 `src/db/connection.py`**

```python
"""SQLite 資料庫連線管理與 Schema 初始化。"""

import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "vocab.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL,
    markdown_body TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS note_attributes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    note_id INTEGER NOT NULL,
    attr_key TEXT NOT NULL,
    attr_value TEXT NOT NULL DEFAULT '',
    UNIQUE(note_id, attr_key),
    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS decks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    note_id INTEGER NOT NULL,
    deck_id INTEGER NOT NULL,
    prompt_field TEXT NOT NULL,
    answer_field TEXT NOT NULL,
    match_mode TEXT NOT NULL DEFAULT 'loose',
    fsrs_state_json TEXT NOT NULL,
    due_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE,
    FOREIGN KEY (deck_id) REFERENCES decks(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS review_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    user_answer TEXT NOT NULL DEFAULT '',
    is_correct INTEGER,
    fsrs_log_json TEXT NOT NULL,
    reviewed_at TEXT NOT NULL,
    FOREIGN KEY (card_id) REFERENCES cards(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_cards_due_at ON cards(due_at);
CREATE INDEX IF NOT EXISTS idx_cards_deck_id ON cards(deck_id);
CREATE INDEX IF NOT EXISTS idx_note_attributes_note_id ON note_attributes(note_id);
"""


def get_connection(db_path: str | Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """取得已啟用外鍵與 Row factory 的 SQLite 連線。"""
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: str | Path = DEFAULT_DB_PATH) -> None:
    """初始化資料庫所有資料表與索引。"""
    with get_connection(db_path) as conn:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
```

- [ ] **Step 4: 執行測試驗證通過**

Run: `.\.venv\Scripts\pytest.exe tests/test_db.py -v`
Expected: `2 passed`

- [ ] **Step 5: Commit**

```bash
git add tests/__init__.py tests/test_db.py src/db/connection.py
git commit -m "feat(db): add SQLite connection helper and schema initialization"
```

---

### Task 3: 資料存取層 Repositories (`src/db/repositories.py`)

**Files:**
- Create: `src/db/repositories.py`
- Modify: `tests/test_db.py` (新增 Repository CRUD 測試)

**Interfaces:**
- Consumes: `get_connection`, `init_db` from `src.db.connection`
- Produces:
  - `NoteRepository(db_path)`: `create_note`, `get_note_by_id`, `find_notes`, `update_note`, `delete_note`, `upsert_attribute`, `get_attributes`
  - `DeckRepository(db_path)`: `create_deck`, `get_deck_by_id`, `get_deck_by_name`, `list_decks`, `delete_deck`
  - `CardRepository(db_path)`: `create_card`, `get_card_by_id`, `list_cards_by_note`, `list_cards_by_deck`, `list_due_cards`, `update_card_schedule`, `delete_card`
  - `ReviewLogRepository(db_path)`: `add_log`, `list_logs_by_card`

- [ ] **Step 1: 在 `tests/test_db.py` 新增 Repository 失敗測試**

```python
from src.db.repositories import CardRepository, DeckRepository, NoteRepository, ReviewLogRepository


def test_note_deck_card_repository_crud(tmp_path: Path) -> None:
    db_file = tmp_path / "repo.db"
    init_db(db_file)

    note_repo = NoteRepository(db_file)
    deck_repo = DeckRepository(db_file)
    card_repo = CardRepository(db_file)
    log_repo = ReviewLogRepository(db_file)

    note_id = note_repo.create_note("勉強", "毎日日本語を勉強します。", "2026-11-16T00:00:00+00:00")
    note_repo.upsert_attribute(note_id, "meaning", "學習、用功")
    note_repo.upsert_attribute(note_id, "reading", "べんきょう")

    note = note_repo.get_note_by_id(note_id)
    assert note is not None
    assert note["word"] == "勉強"
    assert note_repo.get_attributes(note_id) == {
        "meaning": "學習、用功",
        "reading": "べんきょう",
    }

    deck_id = deck_repo.create_deck("日文 N5", "基礎單字", "2026-11-16T00:00:00+00:00")
    card_id = card_repo.create_card(
        note_id=note_id,
        deck_id=deck_id,
        prompt_field="word",
        answer_field="meaning",
        match_mode="loose",
        fsrs_state_json='{"card_id": 1}',
        due_at="2026-11-16T00:00:00+00:00",
        created_at="2026-11-16T00:00:00+00:00",
    )

    due_cards = card_repo.list_due_cards(now_iso="2026-11-16T01:00:00+00:00", deck_id=deck_id)
    assert len(due_cards) == 1
    assert due_cards[0]["id"] == card_id

    log_repo.add_log(
        card_id=card_id,
        rating=3,
        user_answer="學習、用功",
        is_correct=True,
        fsrs_log_json='{"rating": 3}',
        reviewed_at="2026-11-16T00:05:00+00:00",
    )
    logs = log_repo.list_logs_by_card(card_id)
    assert len(logs) == 1
    assert logs[0]["rating"] == 3
```

- [ ] **Step 2: 執行測試確認失敗**

Run: `.\.venv\Scripts\pytest.exe tests/test_db.py::test_note_deck_card_repository_crud -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'src.db.repositories'`

- [ ] **Step 3: 實作 `src/db/repositories.py`**

```python
"""SQLite 資料存取層 (Repositories)。"""

from pathlib import Path
from typing import Any

from src.db.connection import DEFAULT_DB_PATH, get_connection


class _BaseRepository:
    def __init__(self, db_path: str | Path = DEFAULT_DB_PATH) -> None:
        self.db_path = Path(db_path)


class NoteRepository(_BaseRepository):
    """管理 notes 與 note_attributes 資料表。"""

    def create_note(self, word: str, markdown_body: str, now_iso: str) -> int:
        with get_connection(self.db_path) as conn:
            cur = conn.execute(
                """
                INSERT INTO notes (word, markdown_body, created_at, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                (word, markdown_body, now_iso, now_iso),
            )
            conn.commit()
            return int(cur.lastrowid)

    def get_note_by_id(self, note_id: int) -> dict[str, Any] | None:
        with get_connection(self.db_path) as conn:
            row = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
            return dict(row) if row else None

    def find_notes(self, keyword: str = "") -> list[dict[str, Any]]:
        with get_connection(self.db_path) as conn:
            if keyword:
                pattern = f"%{keyword}%"
                rows = conn.execute(
                    """
                    SELECT DISTINCT n.* FROM notes n
                    LEFT JOIN note_attributes a ON n.id = a.note_id
                    WHERE n.word LIKE ? OR n.markdown_body LIKE ? OR a.attr_value LIKE ?
                    ORDER BY n.updated_at DESC, n.id DESC
                    """,
                    (pattern, pattern, pattern),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM notes ORDER BY updated_at DESC, id DESC"
                ).fetchall()
            return [dict(r) for r in rows]

    def update_note(self, note_id: int, word: str, markdown_body: str, now_iso: str) -> bool:
        with get_connection(self.db_path) as conn:
            cur = conn.execute(
                """
                UPDATE notes
                SET word = ?, markdown_body = ?, updated_at = ?
                WHERE id = ?
                """,
                (word, markdown_body, now_iso, note_id),
            )
            conn.commit()
            return cur.rowcount > 0

    def delete_note(self, note_id: int) -> bool:
        with get_connection(self.db_path) as conn:
            cur = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            conn.commit()
            return cur.rowcount > 0

    def upsert_attribute(self, note_id: int, attr_key: str, attr_value: str) -> None:
        with get_connection(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO note_attributes (note_id, attr_key, attr_value)
                VALUES (?, ?, ?)
                ON CONFLICT(note_id, attr_key) DO UPDATE SET attr_value = excluded.attr_value
                """,
                (note_id, attr_key, attr_value),
            )
            conn.commit()

    def get_attributes(self, note_id: int) -> dict[str, str]:
        with get_connection(self.db_path) as conn:
            rows = conn.execute(
                "SELECT attr_key, attr_value FROM note_attributes WHERE note_id = ?",
                (note_id,),
            ).fetchall()
            return {row["attr_key"]: row["attr_value"] for row in rows}


class DeckRepository(_BaseRepository):
    """管理 decks 資料表。"""

    def create_deck(self, name: str, description: str, now_iso: str) -> int:
        with get_connection(self.db_path) as conn:
            cur = conn.execute(
                "INSERT INTO decks (name, description, created_at) VALUES (?, ?, ?)",
                (name, description, now_iso),
            )
            conn.commit()
            return int(cur.lastrowid)

    def get_deck_by_id(self, deck_id: int) -> dict[str, Any] | None:
        with get_connection(self.db_path) as conn:
            row = conn.execute("SELECT * FROM decks WHERE id = ?", (deck_id,)).fetchone()
            return dict(row) if row else None

    def get_deck_by_name(self, name: str) -> dict[str, Any] | None:
        with get_connection(self.db_path) as conn:
            row = conn.execute("SELECT * FROM decks WHERE name = ?", (name,)).fetchone()
            return dict(row) if row else None

    def list_decks(self) -> list[dict[str, Any]]:
        with get_connection(self.db_path) as conn:
            rows = conn.execute("SELECT * FROM decks ORDER BY id ASC").fetchall()
            return [dict(r) for r in rows]

    def delete_deck(self, deck_id: int) -> bool:
        with get_connection(self.db_path) as conn:
            cur = conn.execute("DELETE FROM decks WHERE id = ?", (deck_id,))
            conn.commit()
            return cur.rowcount > 0


class CardRepository(_BaseRepository):
    """管理 cards 資料表。"""

    def create_card(
        self,
        note_id: int,
        deck_id: int,
        prompt_field: str,
        answer_field: str,
        match_mode: str,
        fsrs_state_json: str,
        due_at: str,
        created_at: str,
    ) -> int:
        with get_connection(self.db_path) as conn:
            cur = conn.execute(
                """
                INSERT INTO cards (
                    note_id, deck_id, prompt_field, answer_field,
                    match_mode, fsrs_state_json, due_at, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    note_id,
                    deck_id,
                    prompt_field,
                    answer_field,
                    match_mode,
                    fsrs_state_json,
                    due_at,
                    created_at,
                ),
            )
            conn.commit()
            return int(cur.lastrowid)

    def get_card_by_id(self, card_id: int) -> dict[str, Any] | None:
        with get_connection(self.db_path) as conn:
            row = conn.execute("SELECT * FROM cards WHERE id = ?", (card_id,)).fetchone()
            return dict(row) if row else None

    def list_cards_by_note(self, note_id: int) -> list[dict[str, Any]]:
        with get_connection(self.db_path) as conn:
            rows = conn.execute(
                "SELECT * FROM cards WHERE note_id = ? ORDER BY id ASC", (note_id,)
            ).fetchall()
            return [dict(r) for r in rows]

    def list_cards_by_deck(self, deck_id: int) -> list[dict[str, Any]]:
        with get_connection(self.db_path) as conn:
            rows = conn.execute(
                "SELECT * FROM cards WHERE deck_id = ? ORDER BY due_at ASC, id ASC",
                (deck_id,),
            ).fetchall()
            return [dict(r) for r in rows]

    def list_due_cards(self, now_iso: str, deck_id: int | None = None) -> list[dict[str, Any]]:
        with get_connection(self.db_path) as conn:
            if deck_id is not None:
                rows = conn.execute(
                    """
                    SELECT * FROM cards
                    WHERE due_at <= ? AND deck_id = ?
                    ORDER BY due_at ASC, id ASC
                    """,
                    (now_iso, deck_id),
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT * FROM cards
                    WHERE due_at <= ?
                    ORDER BY due_at ASC, id ASC
                    """,
                    (now_iso,),
                ).fetchall()
            return [dict(r) for r in rows]

    def update_card_schedule(self, card_id: int, fsrs_state_json: str, due_at: str) -> bool:
        with get_connection(self.db_path) as conn:
            cur = conn.execute(
                "UPDATE cards SET fsrs_state_json = ?, due_at = ? WHERE id = ?",
                (fsrs_state_json, due_at, card_id),
            )
            conn.commit()
            return cur.rowcount > 0

    def delete_card(self, card_id: int) -> bool:
        with get_connection(self.db_path) as conn:
            cur = conn.execute("DELETE FROM cards WHERE id = ?", (card_id,))
            conn.commit()
            return cur.rowcount > 0


class ReviewLogRepository(_BaseRepository):
    """管理 review_logs 資料表。"""

    def add_log(
        self,
        card_id: int,
        rating: int,
        user_answer: str,
        is_correct: bool | None,
        fsrs_log_json: str,
        reviewed_at: str,
    ) -> int:
        correct_int = None if is_correct is None else (1 if is_correct else 0)
        with get_connection(self.db_path) as conn:
            cur = conn.execute(
                """
                INSERT INTO review_logs (
                    card_id, rating, user_answer, is_correct, fsrs_log_json, reviewed_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (card_id, rating, user_answer, correct_int, fsrs_log_json, reviewed_at),
            )
            conn.commit()
            return int(cur.lastrowid)

    def list_logs_by_card(self, card_id: int) -> list[dict[str, Any]]:
        with get_connection(self.db_path) as conn:
            rows = conn.execute(
                "SELECT * FROM review_logs WHERE card_id = ? ORDER BY reviewed_at DESC, id DESC",
                (card_id,),
            ).fetchall()
            return [dict(r) for r in rows]
```

- [ ] **Step 4: 執行測試驗證通過**

Run: `.\.venv\Scripts\pytest.exe tests/test_db.py -v`
Expected: `3 passed`

- [ ] **Step 5: Commit**

```bash
git add src/db/repositories.py tests/test_db.py
git commit -m "feat(db): implement Note, Deck, Card, and ReviewLog repositories"
```

---

### Task 4: 答案正規化與嚴格/寬鬆比對 (`src/services/answer_matcher.py`)

**Files:**
- Create: `src/services/answer_matcher.py`
- Create: `tests/test_answer_matcher.py`

**Interfaces:**
- Produces:
  - `MatchResult(is_correct: bool, normalized_user: str, normalized_expected: str)`
  - `normalize_text(text: str, *, mode: str = "loose") -> str`
  - `compare_answer(user_answer: str, expected_answer: str, mode: str = "loose") -> MatchResult`

- [ ] **Step 1: 撰寫失敗測試 `tests/test_answer_matcher.py`**

```python
"""測試答案正規化與嚴格/寬鬆比對邏輯。"""

from src.services.answer_matcher import compare_answer, normalize_text


def test_loose_match_handles_spaces_fullwidth_and_case() -> None:
    assert normalize_text("  Ａｐｐｌｅ  ", mode="loose") == "apple"
    res = compare_answer("  Ａｐｐｌｅ　", "apple", mode="loose")
    assert res.is_correct is True


def test_strict_match_preserves_case_and_fullwidth_differences() -> None:
    res_case = compare_answer("Apple", "apple", mode="strict")
    assert res_case.is_correct is False

    res_exact = compare_answer(" べんきょう ", "べんきょう", mode="strict")
    assert res_exact.is_correct is True
```

- [ ] **Step 2: 執行測試確認失敗**

Run: `.\.venv\Scripts\pytest.exe tests/test_answer_matcher.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'src.services.answer_matcher'`

- [ ] **Step 3: 實作 `src/services/answer_matcher.py`**

```python
"""答案正規化與嚴格/寬鬆比對服務。"""

import re
import unicodedata
from dataclasses import dataclass

VALID_MATCH_MODES = {"strict", "loose", "self_check"}


@dataclass(frozen=True)
class MatchResult:
    """答案比對結果。"""

    is_correct: bool
    normalized_user: str
    normalized_expected: str


def normalize_text(text: str, *, mode: str = "loose") -> str:
    """依比對模式正規化文字（strict 僅去除前後空白；loose 額外做 NFKC 全半形與小寫轉換）。"""
    if mode == "strict":
        return unicodedata.normalize("NFC", text.strip())
    nfkc = unicodedata.normalize("NFKC", text)
    collapsed = re.sub(r"\s+", " ", nfkc).strip()
    return collapsed.casefold()


def compare_answer(user_answer: str, expected_answer: str, mode: str = "loose") -> MatchResult:
    """比對使用者輸入與預期答案。"""
    if mode not in VALID_MATCH_MODES:
        raise ValueError(f"不支援的比對模式: {mode}")
    norm_user = normalize_text(user_answer, mode=mode)
    norm_expected = normalize_text(expected_answer, mode=mode)
    return MatchResult(
        is_correct=(norm_user == norm_expected),
        normalized_user=norm_user,
        normalized_expected=norm_expected,
    )
```

- [ ] **Step 4: 執行測試驗證通過**

Run: `.\.venv\Scripts\pytest.exe tests/test_answer_matcher.py -v`
Expected: `2 passed`

- [ ] **Step 5: Commit**

```bash
git add src/services/answer_matcher.py tests/test_answer_matcher.py
git commit -m "feat(services): add answer normalization and strict/loose matcher"
```

---

### Task 5: 筆記管理服務 (`src/services/note_service.py`) 與卡組/卡片服務 (`src/services/deck_card_service.py`)

**Files:**
- Create: `src/services/note_service.py`
- Create: `src/services/deck_card_service.py`
- Create: `tests/test_note_service.py`
- Create: `tests/test_deck_card_service.py`

**Interfaces:**
- Consumes: `NoteRepository`, `DeckRepository`, `CardRepository` from `src.db.repositories`
- Produces:
  - `FIXED_ATTR_KEYS = ("meaning", "reading", "source", "example")`
  - `NoteDetail(id: int, word: str, markdown_body: str, attributes: dict[str, str], created_at: str, updated_at: str)`
  - `NoteService(db_path)`: `create_note`, `get_note`, `search_notes`, `update_note`, `delete_note`
  - `DeckCardService(db_path)`: `create_deck`, `get_or_create_deck`, `list_decks`, `delete_deck`, `create_card`, `list_cards_by_note`, `list_cards_by_deck`, `delete_card`

- [ ] **Step 1: 撰寫失敗測試 `tests/test_note_service.py` 與 `tests/test_deck_card_service.py`**

`tests/test_note_service.py`:
```python
"""測試筆記與結構化屬性管理服務。"""

from pathlib import Path

from src.db.connection import init_db
from src.services.note_service import NoteService


def test_create_search_and_update_note_preserves_id(tmp_path: Path) -> None:
    db_file = tmp_path / "notes.db"
    init_db(db_file)
    svc = NoteService(db_file)

    note_id = svc.create_note(
        word="勉強",
        markdown_body="## 例句\n毎日日本語を勉強します。",
        attributes={"meaning": "學習", "reading": "べんきょう", "source": "第3課"},
    )

    found = svc.search_notes("べんきょう")
    assert len(found) == 1
    assert found[0].id == note_id
    assert found[0].attributes["meaning"] == "學習"

    svc.update_note(
        note_id=note_id,
        word="勉強する",
        markdown_body="動詞用法",
        attributes={"meaning": "學習、用功", "reading": "べんきょうする"},
    )
    updated = svc.get_note(note_id)
    assert updated is not None
    assert updated.id == note_id
    assert updated.word == "勉強する"
    assert updated.attributes["meaning"] == "學習、用功"
```

`tests/test_deck_card_service.py`:
```python
"""測試卡組管理與一筆記多卡片衍生服務。"""

from pathlib import Path

from src.db.connection import init_db
from src.services.deck_card_service import DeckCardService
from src.services.note_service import NoteService


def test_one_note_generates_multiple_cards_and_keeps_progress_on_note_rename(tmp_path: Path) -> None:
    db_file = tmp_path / "cards.db"
    init_db(db_file)
    note_svc = NoteService(db_file)
    deck_svc = DeckCardService(db_file)

    note_id = note_svc.create_note(
        word="勉強",
        markdown_body="例句",
        attributes={"meaning": "學習", "reading": "べんきょう"},
    )
    deck_id = deck_svc.create_deck("日文課", "第 3 課")

    card_a = deck_svc.create_card(note_id, deck_id, prompt_field="word", answer_field="meaning", match_mode="self_check")
    card_b = deck_svc.create_card(note_id, deck_id, prompt_field="word", answer_field="reading", match_mode="strict")

    assert card_a != card_b
    assert len(deck_svc.list_cards_by_note(note_id)) == 2

    note_svc.update_note(note_id, word="勉強（名・サ変）", markdown_body="更新後的筆記", attributes={"meaning": "學習", "reading": "べんきょう"})
    cards_after = deck_svc.list_cards_by_deck(deck_id)
    assert len(cards_after) == 2
```

- [ ] **Step 2: 執行測試確認失敗**

Run: `.\.venv\Scripts\pytest.exe tests/test_note_service.py tests/test_deck_card_service.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: 實作 `src/services/note_service.py` 與 `src/services/deck_card_service.py`**

`src/services/note_service.py`:
```python
"""筆記與結構化屬性管理服務。"""

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from src.db.connection import DEFAULT_DB_PATH
from src.db.repositories import NoteRepository

FIXED_ATTR_KEYS = ("meaning", "reading", "source", "example")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class NoteDetail:
    """包含結構化屬性的完整單字筆記資料結構。"""

    id: int
    word: str
    markdown_body: str
    attributes: dict[str, str]
    created_at: str
    updated_at: str


class NoteService:
    """提供 CLI 與 GUI 共用的筆記 CRUD 與搜尋功能。"""

    def __init__(self, db_path: str | Path = DEFAULT_DB_PATH) -> None:
        self.repo = NoteRepository(db_path)

    def create_note(
        self,
        word: str,
        markdown_body: str = "",
        attributes: dict[str, str] | None = None,
    ) -> int:
        clean_word = word.strip()
        if not clean_word:
            raise ValueError("單字標題不可為空")
        now_iso = _utc_now_iso()
        note_id = self.repo.create_note(clean_word, markdown_body, now_iso)
        for key, value in (attributes or {}).items():
            self.repo.upsert_attribute(note_id, key.strip(), value.strip())
        return note_id

    def get_note(self, note_id: int) -> NoteDetail | None:
        row = self.repo.get_note_by_id(note_id)
        if not row:
            return None
        attrs = self.repo.get_attributes(note_id)
        return NoteDetail(
            id=row["id"],
            word=row["word"],
            markdown_body=row["markdown_body"],
            attributes=attrs,
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def search_notes(self, keyword: str = "") -> list[NoteDetail]:
        rows = self.repo.find_notes(keyword.strip())
        return [
            NoteDetail(
                id=r["id"],
                word=r["word"],
                markdown_body=r["markdown_body"],
                attributes=self.repo.get_attributes(r["id"]),
                created_at=r["created_at"],
                updated_at=r["updated_at"],
            )
            for r in rows
        ]

    def update_note(
        self,
        note_id: int,
        word: str,
        markdown_body: str,
        attributes: dict[str, str] | None = None,
    ) -> bool:
        clean_word = word.strip()
        if not clean_word:
            raise ValueError("單字標題不可為空")
        ok = self.repo.update_note(note_id, clean_word, markdown_body, _utc_now_iso())
        if not ok:
            return False
        if attributes is not None:
            for key, value in attributes.items():
                self.repo.upsert_attribute(note_id, key.strip(), value.strip())
        return True

    def delete_note(self, note_id: int) -> bool:
        return self.repo.delete_note(note_id)
```

`src/services/deck_card_service.py`:
```python
"""卡組管理與卡片生成服務。"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fsrs import Card

from src.db.connection import DEFAULT_DB_PATH
from src.db.repositories import CardRepository, DeckRepository, NoteRepository
from src.services.answer_matcher import VALID_MATCH_MODES

VALID_CARD_FIELDS = {"word", "meaning", "reading", "source", "example"}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class DeckCardService:
    """管理卡組與從單字筆記衍生的複習卡片。"""

    def __init__(self, db_path: str | Path = DEFAULT_DB_PATH) -> None:
        self.deck_repo = DeckRepository(db_path)
        self.card_repo = CardRepository(db_path)
        self.note_repo = NoteRepository(db_path)

    def create_deck(self, name: str, description: str = "") -> int:
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("卡組名稱不可為空")
        return self.deck_repo.create_deck(clean_name, description.strip(), _utc_now_iso())

    def get_or_create_deck(self, name: str, description: str = "") -> int:
        existing = self.deck_repo.get_deck_by_name(name.strip())
        if existing:
            return int(existing["id"])
        return self.create_deck(name, description)

    def list_decks(self) -> list[dict[str, Any]]:
        return self.deck_repo.list_decks()

    def delete_deck(self, deck_id: int) -> bool:
        return self.deck_repo.delete_deck(deck_id)

    def create_card(
        self,
        note_id: int,
        deck_id: int,
        prompt_field: str = "word",
        answer_field: str = "meaning",
        match_mode: str = "loose",
    ) -> int:
        if prompt_field not in VALID_CARD_FIELDS or answer_field not in VALID_CARD_FIELDS:
            raise ValueError(f"卡片欄位必須屬於 {VALID_CARD_FIELDS}")
        if match_mode not in VALID_MATCH_MODES:
            raise ValueError(f"比對模式必須屬於 {VALID_MATCH_MODES}")
        if not self.note_repo.get_note_by_id(note_id):
            raise ValueError(f"找不到筆記 ID={note_id}")
        if not self.deck_repo.get_deck_by_id(deck_id):
            raise ValueError(f"找不到卡組 ID={deck_id}")

        fsrs_card = Card()
        now_iso = _utc_now_iso()
        due_iso = fsrs_card.due.isoformat()
        return self.card_repo.create_card(
            note_id=note_id,
            deck_id=deck_id,
            prompt_field=prompt_field,
            answer_field=answer_field,
            match_mode=match_mode,
            fsrs_state_json=json.dumps(fsrs_card.to_dict()),
            due_at=due_iso,
            created_at=now_iso,
        )

    def list_cards_by_note(self, note_id: int) -> list[dict[str, Any]]:
        return self.card_repo.list_cards_by_note(note_id)

    def list_cards_by_deck(self, deck_id: int) -> list[dict[str, Any]]:
        return self.card_repo.list_cards_by_deck(deck_id)

    def delete_card(self, card_id: int) -> bool:
        return self.card_repo.delete_card(card_id)
```

- [ ] **Step 4: 執行測試驗證通過**

Run: `.\.venv\Scripts\pytest.exe tests/test_note_service.py tests/test_deck_card_service.py -v`
Expected: `2 passed`

- [ ] **Step 5: Commit**

```bash
git add src/services/note_service.py src/services/deck_card_service.py tests/test_note_service.py tests/test_deck_card_service.py
git commit -m "feat(services): add NoteService and DeckCardService"
```

---

## 階段二：複習引擎與 Py-FSRS 排程 (`src/services/review_service.py`)

### Task 6: 複習排程服務 (`src/services/review_service.py`)

**Files:**
- Create: `src/services/review_service.py`
- Create: `tests/test_review_service.py`

**Interfaces:**
- Consumes: `CardRepository`, `NoteRepository`, `ReviewLogRepository` from `src.db.repositories`; `compare_answer`, `MatchResult` from `src.services.answer_matcher`
- Produces:
  - `DueCardView(card_id: int, note_id: int, deck_id: int, word: str, prompt_field: str, prompt_text: str, answer_field: str, expected_answer: str, match_mode: str, due_at: str)`
  - `ReviewService(db_path)`:
    - `get_due_cards(deck_id: int | None = None, now: datetime | None = None) -> list[DueCardView]`
    - `check_answer(card_id: int, user_answer: str) -> MatchResult`
    - `submit_review(card_id: int, rating_value: int, user_answer: str = "", is_correct: bool | None = None, now: datetime | None = None) -> str` (回傳新的 `due_at` ISO 字串)

- [ ] **Step 1: 撰寫失敗測試 `tests/test_review_service.py`**

```python
"""測試到期卡片挑選與 Py-FSRS 排程更新服務。"""

from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.db.connection import init_db
from src.services.deck_card_service import DeckCardService
from src.services.note_service import NoteService
from src.services.review_service import ReviewService


def test_review_flow_updates_fsrs_due_date_and_writes_log(tmp_path: Path) -> None:
    db_file = tmp_path / "review.db"
    init_db(db_file)
    note_svc = NoteService(db_file)
    deck_svc = DeckCardService(db_file)
    review_svc = ReviewService(db_file)

    note_id = note_svc.create_note(
        word="勉強",
        markdown_body="例句",
        attributes={"meaning": "學習", "reading": "べんきょう"},
    )
    deck_id = deck_svc.create_deck("日文")
    card_id = deck_svc.create_card(note_id, deck_id, prompt_field="word", answer_field="reading", match_mode="strict")

    now = datetime.now(timezone.utc) + timedelta(minutes=1)
    due = review_svc.get_due_cards(deck_id=deck_id, now=now)
    assert len(due) == 1
    assert due[0].prompt_text == "勉強"
    assert due[0].expected_answer == "べんきょう"

    match_res = review_svc.check_answer(card_id, "べんきょう")
    assert match_res.is_correct is True

    next_due_iso = review_svc.submit_review(
        card_id=card_id,
        rating_value=4,  # Easy
        user_answer="べんきょう",
        is_correct=match_res.is_correct,
        now=now,
    )
    assert datetime.fromisoformat(next_due_iso) > now
    assert len(review_svc.log_repo.list_logs_by_card(card_id)) == 1
```

- [ ] **Step 2: 執行測試確認失敗**

Run: `.\.venv\Scripts\pytest.exe tests/test_review_service.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'src.services.review_service'`

- [ ] **Step 3: 實作 `src/services/review_service.py`**

```python
"""到期卡片挑選、作答比對與 Py-FSRS 排程服務。"""

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from fsrs import Card, Rating, Scheduler

from src.db.connection import DEFAULT_DB_PATH
from src.db.repositories import CardRepository, NoteRepository, ReviewLogRepository
from src.services.answer_matcher import MatchResult, compare_answer

RATING_MAP: dict[int, Rating] = {
    1: Rating.Again,
    2: Rating.Hard,
    3: Rating.Good,
    4: Rating.Easy,
}


@dataclass(frozen=True)
class DueCardView:
    """複習畫面所需的卡片檢視資料。"""

    card_id: int
    note_id: int
    deck_id: int
    word: str
    prompt_field: str
    prompt_text: str
    answer_field: str
    expected_answer: str
    match_mode: str
    due_at: str


class ReviewService:
    """整合 Py-FSRS 與資料庫的複習流程服務。"""

    def __init__(self, db_path: str | Path = DEFAULT_DB_PATH) -> None:
        self.card_repo = CardRepository(db_path)
        self.note_repo = NoteRepository(db_path)
        self.log_repo = ReviewLogRepository(db_path)
        self.scheduler = Scheduler()

    def _resolve_field(self, note: dict, attrs: dict[str, str], field: str) -> str:
        if field == "word":
            return str(note["word"])
        return attrs.get(field, "")

    def get_due_cards(
        self,
        deck_id: int | None = None,
        now: datetime | None = None,
    ) -> list[DueCardView]:
        current = now or datetime.now(timezone.utc)
        rows = self.card_repo.list_due_cards(current.isoformat(), deck_id=deck_id)
        views: list[DueCardView] = []
        for row in rows:
            note = self.note_repo.get_note_by_id(row["note_id"])
            if not note:
                continue
            attrs = self.note_repo.get_attributes(row["note_id"])
            views.append(
                DueCardView(
                    card_id=row["id"],
                    note_id=row["note_id"],
                    deck_id=row["deck_id"],
                    word=note["word"],
                    prompt_field=row["prompt_field"],
                    prompt_text=self._resolve_field(note, attrs, row["prompt_field"]),
                    answer_field=row["answer_field"],
                    expected_answer=self._resolve_field(note, attrs, row["answer_field"]),
                    match_mode=row["match_mode"],
                    due_at=row["due_at"],
                )
            )
        return views

    def check_answer(self, card_id: int, user_answer: str) -> MatchResult:
        card_row = self.card_repo.get_card_by_id(card_id)
        if not card_row:
            raise ValueError(f"找不到卡片 ID={card_id}")
        note = self.note_repo.get_note_by_id(card_row["note_id"])
        if not note:
            raise ValueError(f"找不到對應筆記 ID={card_row['note_id']}")
        attrs = self.note_repo.get_attributes(card_row["note_id"])
        expected = self._resolve_field(note, attrs, card_row["answer_field"])
        mode = "loose" if card_row["match_mode"] == "self_check" else card_row["match_mode"]
        return compare_answer(user_answer, expected, mode=mode)

    def submit_review(
        self,
        card_id: int,
        rating_value: int,
        user_answer: str = "",
        is_correct: bool | None = None,
        now: datetime | None = None,
    ) -> str:
        if rating_value not in RATING_MAP:
            raise ValueError("評分必須為 1(忘記)、2(困難)、3(記得) 或 4(簡單)")
        card_row = self.card_repo.get_card_by_id(card_id)
        if not card_row:
            raise ValueError(f"找不到卡片 ID={card_id}")

        review_dt = now or datetime.now(timezone.utc)
        fsrs_card = Card.from_dict(json.loads(card_row["fsrs_state_json"]))
        updated_card, review_log = self.scheduler.review_card(
            card=fsrs_card,
            rating=RATING_MAP[rating_value],
            review_datetime=review_dt,
        )

        new_due_iso = updated_card.due.isoformat()
        self.card_repo.update_card_schedule(
            card_id=card_id,
            fsrs_state_json=json.dumps(updated_card.to_dict()),
            due_at=new_due_iso,
        )
        self.log_repo.add_log(
            card_id=card_id,
            rating=rating_value,
            user_answer=user_answer,
            is_correct=is_correct,
            fsrs_log_json=json.dumps(review_log.to_dict()),
            reviewed_at=review_dt.isoformat(),
        )
        return new_due_iso
```

- [ ] **Step 4: 執行測試驗證通過**

Run: `.\.venv\Scripts\pytest.exe tests/test_review_service.py -v`
Expected: `1 passed`

- [ ] **Step 5: Commit**

```bash
git add src/services/review_service.py tests/test_review_service.py
git commit -m "feat(services): integrate Py-FSRS review scheduling and log persistence"
```

---

## 階段三：Markdown 預覽與 CSV 匯入匯出

### Task 7: Markdown 轉 HTML 與瀏覽器預覽 (`src/services/markdown_service.py`)

**Files:**
- Create: `src/services/markdown_service.py`
- Create: `tests/test_markdown_service.py`

**Interfaces:**
- Produces:
  - `render_note_html(word: str, attributes: dict[str, str], markdown_body: str) -> str`
  - `save_and_open_preview(html_content: str, output_path: Path | None = None, open_browser: bool = True) -> Path`

- [ ] **Step 1: 撰寫失敗測試 `tests/test_markdown_service.py`**

```python
"""測試 Markdown 筆記 HTML 預覽生成。"""

from pathlib import Path

from src.services.markdown_service import render_note_html, save_and_open_preview


def test_render_note_html_contains_word_attributes_and_markdown(tmp_path: Path) -> None:
    html = render_note_html(
        word="勉強",
        attributes={"meaning": "學習", "reading": "べんきょう"},
        markdown_body="## 例句\n- 毎日日本語を**勉強**します。",
    )
    assert "勉強" in html
    assert "學習" in html
    assert "<strong>勉強</strong>" in html

    out_file = tmp_path / "preview.html"
    saved = save_and_open_preview(html, output_path=out_file, open_browser=False)
    assert saved.exists()
    assert "べんきょう" in saved.read_text(encoding="utf-8")
```

- [ ] **Step 2: 執行測試確認失敗**

Run: `.\.venv\Scripts\pytest.exe tests/test_markdown_service.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: 實作 `src/services/markdown_service.py`**

```python
"""Markdown 筆記轉 HTML 與瀏覽器預覽服務。"""

import html
import tempfile
import webbrowser
from pathlib import Path

import markdown


def render_note_html(
    word: str,
    attributes: dict[str, str],
    markdown_body: str,
) -> str:
    """將單字標題、結構化屬性與 Markdown 本文轉為完整 HTML 文件。"""
    body_html = markdown.markdown(markdown_body or "", extensions=["tables", "fenced_code"])
    attr_rows = "".join(
        f"<tr><th>{html.escape(k)}</th><td>{html.escape(v)}</td></tr>"
        for k, v in attributes.items()
        if v
    )
    attr_table = f"<table>{attr_rows}</table>" if attr_rows else ""

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<title>{html.escape(word)} - 單字筆記預覽</title>
<style>
  body {{ font-family: "Microsoft JhengHei", sans-serif; max-width: 760px; margin: 40px auto; padding: 0 20px; line-height: 1.7; color: #222; }}
  h1 {{ color: #1E3A34; border-bottom: 2px solid #3F8F7A; padding-bottom: 8px; }}
  table {{ width: 100%; border-collapse: collapse; margin: 16px 0; }}
  th, td {{ border: 1px solid #d5e0dc; padding: 8px 12px; text-align: left; }}
  th {{ background: #eef3f0; width: 140px; color: #1E3A34; }}
  pre {{ background: #f5f7f6; padding: 12px; border-radius: 6px; overflow-x: auto; }}
</style>
</head>
<body>
  <h1>{html.escape(word)}</h1>
  {attr_table}
  <div class="markdown-body">{body_html}</div>
</body>
</html>
"""


def save_and_open_preview(
    html_content: str,
    output_path: Path | None = None,
    open_browser: bool = True,
) -> Path:
    """儲存預覽 HTML 並視需要以系統預設瀏覽器開啟。"""
    if output_path is None:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html", prefix="vocab_preview_")
        target = Path(tmp.name)
        tmp.close()
    else:
        target = Path(output_path)
    target.write_text(html_content, encoding="utf-8")
    if open_browser:
        webbrowser.open(target.resolve().as_uri())
    return target
```

- [ ] **Step 4: 執行測試驗證通過**

Run: `.\.venv\Scripts\pytest.exe tests/test_markdown_service.py -v`
Expected: `1 passed`

- [ ] **Step 5: Commit**

```bash
git add src/services/markdown_service.py tests/test_markdown_service.py
git commit -m "feat(services): add Markdown to HTML preview service"
```

---

### Task 8: CSV 批次匯入與匯出服務 (`src/services/csv_service.py`)

**Files:**
- Create: `src/services/csv_service.py`
- Create: `tests/test_csv_service.py`

**Interfaces:**
- Consumes: `NoteService` from `src.services.note_service`; `DeckCardService` from `src.services.deck_card_service`
- Produces:
  - `CSV_COLUMNS = ("word", "meaning", "reading", "source", "example", "markdown_body", "deck")`
  - `ImportReport(created_notes: int, created_cards: int, skipped_duplicates: int, errors: list[str])`
  - `CsvService(db_path)`:
    - `export_notes(csv_path: str | Path) -> int`
    - `import_notes(csv_path: str | Path, default_deck: str = "Default", create_default_card: bool = True) -> ImportReport`

- [ ] **Step 1: 撰寫失敗測試 `tests/test_csv_service.py`**

```python
"""測試 CSV 批次匯入與匯出服務。"""

from pathlib import Path

from src.db.connection import init_db
from src.services.csv_service import CsvService
from src.services.note_service import NoteService


def test_csv_import_handles_duplicates_and_exports_utf8(tmp_path: Path) -> None:
    db_file = tmp_path / "csv.db"
    init_db(db_file)
    csv_svc = CsvService(db_file)
    note_svc = NoteService(db_file)

    in_csv = tmp_path / "import.csv"
    in_csv.write_text(
        "word,meaning,reading,source,example,markdown_body,deck\n"
        "勉強,學習,べんきょう,第3課,毎日勉強します,筆記內容,日文課\n"
        "勉強,重複詞,べんきょう,第3課,,,日文課\n"
        ",缺單字,test,,,,日文課\n",
        encoding="utf-8",
    )

    report = csv_svc.import_notes(in_csv)
    assert report.created_notes == 1
    assert report.created_cards == 1
    assert report.skipped_duplicates == 1
    assert len(report.errors) == 1
    assert len(note_svc.search_notes("")) == 1

    out_csv = tmp_path / "export.csv"
    count = csv_svc.export_notes(out_csv)
    assert count == 1
    assert "勉強" in out_csv.read_text(encoding="utf-8-sig")
```

- [ ] **Step 2: 執行測試確認失敗**

Run: `.\.venv\Scripts\pytest.exe tests/test_csv_service.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: 實作 `src/services/csv_service.py`**

```python
"""CSV 批次匯入與匯出服務。"""

import csv
from dataclasses import dataclass
from pathlib import Path

from src.db.connection import DEFAULT_DB_PATH
from src.services.deck_card_service import DeckCardService
from src.services.note_service import NoteService

CSV_COLUMNS = ("word", "meaning", "reading", "source", "example", "markdown_body", "deck")


@dataclass(frozen=True)
class ImportReport:
    """CSV 匯入結果摘要。"""

    created_notes: int
    created_cards: int
    skipped_duplicates: int
    errors: list[str]


class CsvService:
    """處理單字筆記與卡組的 CSV 匯入與匯出。"""

    def __init__(self, db_path: str | Path = DEFAULT_DB_PATH) -> None:
        self.note_svc = NoteService(db_path)
        self.deck_svc = DeckCardService(db_path)

    def export_notes(self, csv_path: str | Path) -> int:
        notes = self.note_svc.search_notes("")
        decks_by_id = {d["id"]: d["name"] for d in self.deck_svc.list_decks()}
        target = Path(csv_path)
        target.parent.mkdir(parents=True, exist_ok=True)

        with target.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(CSV_COLUMNS))
            writer.writeheader()
            for note in notes:
                cards = self.deck_svc.list_cards_by_note(note.id)
                deck_name = decks_by_id.get(cards[0]["deck_id"], "") if cards else ""
                writer.writerow(
                    {
                        "word": note.word,
                        "meaning": note.attributes.get("meaning", ""),
                        "reading": note.attributes.get("reading", ""),
                        "source": note.attributes.get("source", ""),
                        "example": note.attributes.get("example", ""),
                        "markdown_body": note.markdown_body,
                        "deck": deck_name,
                    }
                )
        return len(notes)

    def import_notes(
        self,
        csv_path: str | Path,
        default_deck: str = "Default",
        create_default_card: bool = True,
    ) -> ImportReport:
        source_file = Path(csv_path)
        existing_words = {n.word for n in self.note_svc.search_notes("")}
        created_notes = 0
        created_cards = 0
        skipped_duplicates = 0
        errors: list[str] = []

        with source_file.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames or "word" not in reader.fieldnames:
                raise ValueError("CSV 缺少必要欄位: word")

            for idx, row in enumerate(reader, start=2):
                word = (row.get("word") or "").strip()
                if not word:
                    errors.append(f"第 {idx} 列：word 欄位為空，已略過")
                    continue
                if word in existing_words:
                    skipped_duplicates += 1
                    continue

                attrs = {
                    key: (row.get(key) or "").strip()
                    for key in ("meaning", "reading", "source", "example")
                }
                note_id = self.note_svc.create_note(
                    word=word,
                    markdown_body=(row.get("markdown_body") or "").strip(),
                    attributes=attrs,
                )
                existing_words.add(word)
                created_notes += 1

                if create_default_card:
                    deck_name = (row.get("deck") or "").strip() or default_deck
                    deck_id = self.deck_svc.get_or_create_deck(deck_name)
                    self.deck_svc.create_card(
                        note_id=note_id,
                        deck_id=deck_id,
                        prompt_field="word",
                        answer_field="meaning",
                        match_mode="loose",
                    )
                    created_cards += 1

        return ImportReport(
            created_notes=created_notes,
            created_cards=created_cards,
            skipped_duplicates=skipped_duplicates,
            errors=errors,
        )
```

- [ ] **Step 4: 執行測試驗證通過**

Run: `.\.venv\Scripts\pytest.exe tests/test_csv_service.py -v`
Expected: `1 passed`

- [ ] **Step 5: Commit**

```bash
git add src/services/csv_service.py tests/test_csv_service.py
git commit -m "feat(services): add CSV import and export service"
```

---

## 階段四：介面層整合 (CLI、Tkinter GUI、Entry Point 與範例資料)

### Task 9: CLI 命令列介面與互動複習流程 (`src/cli/app.py`)

**Files:**
- Create: `src/cli/app.py`
- Create: `tests/test_cli.py`

**Interfaces:**
- Consumes: `init_db`, `DEFAULT_DB_PATH` from `src.db.connection`; `NoteService`, `DeckCardService`, `ReviewService`, `CsvService` from `src.services.*`
- Produces:
  - `run_cli(argv: list[str] | None = None, db_path: str | Path = DEFAULT_DB_PATH) -> int`

- [ ] **Step 1: 撰寫失敗測試 `tests/test_cli.py`**

```python
"""測試 CLI 指令與互動式複習流程。"""

from pathlib import Path

from src.cli.app import run_cli


def test_cli_note_deck_card_and_review_flow(tmp_path: Path, monkeypatch, capsys) -> None:
    db_file = tmp_path / "cli.db"

    assert run_cli(["note", "add", "勉強", "--meaning", "學習", "--reading", "べんきょう"], db_path=db_file) == 0
    assert run_cli(["deck", "create", "日文"], db_path=db_file) == 0
    assert run_cli(["card", "add", "--note-id", "1", "--deck-id", "1", "--answer-field", "reading", "--mode", "strict"], db_path=db_file) == 0

    inputs = iter(["べんきょう", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert run_cli(["review", "--deck-id", "1"], db_path=db_file) == 0

    out = capsys.readouterr().out
    assert "符合 ✓" in out
```

- [ ] **Step 2: 執行測試確認失敗**

Run: `.\.venv\Scripts\pytest.exe tests/test_cli.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'src.cli.app'`

- [ ] **Step 3: 實作 `src/cli/app.py`**

```python
"""單字筆記與複習系統 - 命令列介面 (CLI)。"""

import argparse
from pathlib import Path

from src.db.connection import DEFAULT_DB_PATH, init_db
from src.services.csv_service import CsvService
from src.services.deck_card_service import DeckCardService
from src.services.note_service import NoteService
from src.services.review_service import ReviewService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vocab --cli", description="單字筆記與複習系統 CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    # note
    note_p = sub.add_parser("note", help="管理單字筆記")
    note_sub = note_p.add_subparsers(dest="action", required=True)

    note_add = note_sub.add_parser("add", help="新增單字筆記")
    note_add.add_argument("word")
    note_add.add_argument("--meaning", default="")
    note_add.add_argument("--reading", default="")
    note_add.add_argument("--source", default="")
    note_add.add_argument("--example", default="")
    note_add.add_argument("--body", default="")

    note_list = note_sub.add_parser("list", help="搜尋或列出筆記")
    note_list.add_argument("--keyword", default="")

    # deck
    deck_p = sub.add_parser("deck", help="管理卡組")
    deck_sub = deck_p.add_subparsers(dest="action", required=True)
    deck_create = deck_sub.add_parser("create", help="建立卡組")
    deck_create.add_argument("name")
    deck_create.add_argument("--desc", default="")
    deck_sub.add_parser("list", help="列出所有卡組")

    # card
    card_p = sub.add_parser("card", help="管理複習卡片")
    card_sub = card_p.add_subparsers(dest="action", required=True)
    card_add = card_sub.add_parser("add", help="從筆記建立卡片")
    card_add.add_argument("--note-id", type=int, required=True)
    card_add.add_argument("--deck-id", type=int, required=True)
    card_add.add_argument("--prompt-field", default="word")
    card_add.add_argument("--answer-field", default="meaning")
    card_add.add_argument("--mode", default="loose")

    # review
    rev_p = sub.add_parser("review", help="開始複習到期卡片")
    rev_p.add_argument("--deck-id", type=int, default=None)

    # csv
    csv_p = sub.add_parser("csv", help="CSV 匯入與匯出")
    csv_sub = csv_p.add_subparsers(dest="action", required=True)
    csv_imp = csv_sub.add_parser("import", help="匯入 CSV")
    csv_imp.add_argument("path")
    csv_exp = csv_sub.add_parser("export", help="匯出 CSV")
    csv_exp.add_argument("path")

    return parser


def run_cli(argv: list[str] | None = None, db_path: str | Path = DEFAULT_DB_PATH) -> int:
    init_db(db_path)
    args = build_parser().parse_args(argv)
    note_svc = NoteService(db_path)
    deck_svc = DeckCardService(db_path)
    review_svc = ReviewService(db_path)
    csv_svc = CsvService(db_path)

    if args.command == "note":
        if args.action == "add":
            nid = note_svc.create_note(
                word=args.word,
                markdown_body=args.body,
                attributes={
                    "meaning": args.meaning,
                    "reading": args.reading,
                    "source": args.source,
                    "example": args.example,
                },
            )
            print(f"已新增筆記 ID={nid}：{args.word}")
        elif args.action == "list":
            for n in note_svc.search_notes(args.keyword):
                print(f"[{n.id}] {n.word} - {n.attributes.get('meaning', '')}")

    elif args.command == "deck":
        if args.action == "create":
            did = deck_svc.create_deck(args.name, args.desc)
            print(f"已建立卡組 ID={did}：{args.name}")
        elif args.action == "list":
            for d in deck_svc.list_decks():
                print(f"[{d['id']}] {d['name']} ({d['description']})")

    elif args.command == "card" and args.action == "add":
        cid = deck_svc.create_card(
            note_id=args.note_id,
            deck_id=args.deck_id,
            prompt_field=args.prompt_field,
            answer_field=args.answer_field,
            match_mode=args.mode,
        )
        print(f"已建立卡片 ID={cid}")

    elif args.command == "review":
        due_cards = review_svc.get_due_cards(deck_id=args.deck_id)
        if not due_cards:
            print("目前沒有到期的卡片。")
            return 0
        for card in due_cards:
            print(f"\n題目 ({card.prompt_field} -> {card.answer_field}): {card.prompt_text}")
            user_ans = input("你的答案（可直接按 Enter 進行自評）：")
            if card.match_mode != "self_check":
                res = review_svc.check_answer(card.card_id, user_ans)
                status = "符合 ✓" if res.is_correct else "不符合 ✗（建議選 1 忘記）"
                print(f"參考答案：{card.expected_answer} | 比對結果：{status}")
            else:
                print(f"參考答案：{card.expected_answer}")
            rating = int(input("FSRS 評分 (1 忘記 / 2 困難 / 3 記得 / 4 簡單)："))
            next_due = review_svc.submit_review(card.card_id, rating, user_answer=user_ans)
            print(f"已更新排程，下次複習時間：{next_due}")

    elif args.command == "csv":
        if args.action == "import":
            rep = csv_svc.import_notes(args.path)
            print(f"匯入完成：新增筆記 {rep.created_notes}、卡片 {rep.created_cards}、重複略過 {rep.skipped_duplicates}")
        elif args.action == "export":
            cnt = csv_svc.export_notes(args.path)
            print(f"已匯出 {cnt} 筆筆記至 {args.path}")

    return 0
```

- [ ] **Step 4: 執行測試驗證通過**

Run: `.\.venv\Scripts\pytest.exe tests/test_cli.py -v`
Expected: `1 passed`

- [ ] **Step 5: Commit**

```bash
git add src/cli/app.py tests/test_cli.py
git commit -m "feat(cli): implement CLI commands and interactive FSRS review loop"
```

---

### Task 10: Tkinter GUI 桌面介面 (`src/gui/app.py`)

**Files:**
- Create: `src/gui/app.py`

**Interfaces:**
- Consumes: `init_db`, `DEFAULT_DB_PATH` from `src.db.connection`; `NoteService`, `DeckCardService`, `ReviewService`, `CsvService`, `render_note_html`, `save_and_open_preview` from `src.services.*`
- Produces:
  - `VocabApp(tk.Tk)`
  - `run_gui(db_path: str | Path = DEFAULT_DB_PATH) -> None`

- [ ] **Step 1: 實作 `src/gui/app.py`（筆記編輯、Markdown 瀏覽器預覽、卡組與複習視窗、CSV 匯入匯出）**

```python
"""單字筆記與複習系統 - Tkinter GUI 桌面介面。"""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

from src.db.connection import DEFAULT_DB_PATH, init_db
from src.services.csv_service import CsvService
from src.services.deck_card_service import DeckCardService
from src.services.markdown_service import render_note_html, save_and_open_preview
from src.services.note_service import FIXED_ATTR_KEYS, NoteService
from src.services.review_service import ReviewService


class VocabApp(tk.Tk):
    """主視窗：左側為搜尋與筆記清單，右側為屬性/Markdown 編輯與複習操作。"""

    def __init__(self, db_path: str | Path = DEFAULT_DB_PATH) -> None:
        super().__init__()
        self.title("單字筆記與複習系統")
        self.geometry("980x660")

        init_db(db_path)
        self.note_svc = NoteService(db_path)
        self.deck_svc = DeckCardService(db_path)
        self.review_svc = ReviewService(db_path)
        self.csv_svc = CsvService(db_path)

        self.current_note_id: int | None = None
        self.note_ids: list[int] = []
        self.attr_vars: dict[str, tk.StringVar] = {k: tk.StringVar() for k in FIXED_ATTR_KEYS}
        self.word_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self._build_menu()
        self._build_layout()
        self._refresh_notes()

    def _build_menu(self) -> None:
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="匯入 CSV...", command=self._on_import_csv)
        file_menu.add_command(label="匯出 CSV...", command=self._on_export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="結束", command=self.destroy)
        menubar.add_cascade(label="檔案", menu=file_menu)

        deck_menu = tk.Menu(menubar, tearoff=0)
        deck_menu.add_command(label="新增卡組...", command=self._on_create_deck)
        deck_menu.add_command(label="開始複習到期卡片", command=self._on_start_review)
        menubar.add_cascade(label="複習與卡組", menu=deck_menu)
        self.config(menu=menubar)

    def _build_layout(self) -> None:
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # 左側清單
        left = ttk.Frame(paned, width=260)
        search_frame = ttk.Frame(left)
        search_frame.pack(fill=tk.X, pady=(0, 6))
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(search_frame, text="搜尋", command=self._refresh_notes).pack(side=tk.LEFT, padx=(4, 0))

        self.listbox = tk.Listbox(left)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self._on_select_note)

        btn_left = ttk.Frame(left)
        btn_left.pack(fill=tk.X, pady=(6, 0))
        ttk.Button(btn_left, text="新增筆記", command=self._on_new_note).pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(btn_left, text="刪除筆記", command=self._on_delete_note).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(4, 0))
        paned.add(left, weight=1)

        # 右側編輯器
        right = ttk.Frame(paned)
        ttk.Label(right, text="單字標題").pack(anchor=tk.W)
        ttk.Entry(right, textvariable=self.word_var).pack(fill=tk.X, pady=(0, 6))

        for key, label in (("meaning", "意思"), ("reading", "讀音"), ("source", "出處"), ("example", "例句")):
            row = ttk.Frame(right)
            row.pack(fill=tk.X, pady=2)
            ttk.Label(row, text=label, width=8).pack(side=tk.LEFT)
            ttk.Entry(row, textvariable=self.attr_vars[key]).pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(right, text="Markdown 筆記本文").pack(anchor=tk.W, pady=(8, 2))
        self.body_text = tk.Text(right, height=14, wrap=tk.WORD)
        self.body_text.pack(fill=tk.BOTH, expand=True)

        actions = ttk.Frame(right)
        actions.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(actions, text="儲存筆記", command=self._on_save_note).pack(side=tk.LEFT)
        ttk.Button(actions, text="瀏覽器預覽 Markdown", command=self._on_preview_markdown).pack(side=tk.LEFT, padx=6)
        ttk.Button(actions, text="衍生複習卡片", command=self._on_create_card_for_note).pack(side=tk.LEFT)
        ttk.Button(actions, text="開始複習", command=self._on_start_review).pack(side=tk.RIGHT)
        paned.add(right, weight=3)

    def _refresh_notes(self) -> None:
        self.listbox.delete(0, tk.END)
        notes = self.note_svc.search_notes(self.search_var.get())
        self.note_ids = [n.id for n in notes]
        for n in notes:
            meaning = n.attributes.get("meaning", "")
            self.listbox.insert(tk.END, f"{n.word}  ({meaning})" if meaning else n.word)

    def _on_select_note(self, _event: tk.Event) -> None:
        sel = self.listbox.curselection()
        if not sel:
            return
        note = self.note_svc.get_note(self.note_ids[sel[0]])
        if not note:
            return
        self.current_note_id = note.id
        self.word_var.set(note.word)
        for key in FIXED_ATTR_KEYS:
            self.attr_vars[key].set(note.attributes.get(key, ""))
        self.body_text.delete("1.0", tk.END)
        self.body_text.insert("1.0", note.markdown_body)

    def _on_new_note(self) -> None:
        self.current_note_id = None
        self.word_var.set("")
        for var in self.attr_vars.values():
            var.set("")
        self.body_text.delete("1.0", tk.END)

    def _on_save_note(self) -> None:
        word = self.word_var.get().strip()
        if not word:
            messagebox.showwarning("欄位錯誤", "單字標題不可為空")
            return
        attrs = {k: v.get().strip() for k, v in self.attr_vars.items()}
        body = self.body_text.get("1.0", tk.END).strip()
        if self.current_note_id is None:
            self.current_note_id = self.note_svc.create_note(word, body, attrs)
        else:
            self.note_svc.update_note(self.current_note_id, word, body, attrs)
        self._refresh_notes()
        messagebox.showinfo("成功", "筆記已儲存")

    def _on_delete_note(self) -> None:
        if self.current_note_id is None:
            return
        if messagebox.askyesno("確認刪除", "確定要刪除此筆記與其所有衍生卡片嗎？"):
            self.note_svc.delete_note(self.current_note_id)
            self._on_new_note()
            self._refresh_notes()

    def _on_preview_markdown(self) -> None:
        attrs = {k: v.get().strip() for k, v in self.attr_vars.items()}
        html_doc = render_note_html(
            word=self.word_var.get().strip() or "未命名單字",
            attributes=attrs,
            markdown_body=self.body_text.get("1.0", tk.END).strip(),
        )
        save_and_open_preview(html_doc, open_browser=True)

    def _on_create_deck(self) -> None:
        name = simpledialog.askstring("新增卡組", "請輸入卡組名稱：")
        if name:
            self.deck_svc.create_deck(name)
            messagebox.showinfo("成功", f"已建立卡組：{name}")

    def _on_create_card_for_note(self) -> None:
        if self.current_note_id is None:
            messagebox.showwarning("提示", "請先儲存或選擇一筆單字筆記")
            return
        deck_id = self.deck_svc.get_or_create_deck("Default")
        answer_field = simpledialog.askstring(
            "衍生卡片",
            "請輸入要測驗的欄位 (meaning / reading / example)：",
            initialvalue="meaning",
        )
        if answer_field in ("meaning", "reading", "example"):
            self.deck_svc.create_card(self.current_note_id, deck_id, "word", answer_field, "loose")
            messagebox.showinfo("成功", f"已建立卡片 (word -> {answer_field})")

    def _on_start_review(self) -> None:
        due = self.review_svc.get_due_cards()
        if not due:
            messagebox.showinfo("複習", "目前沒有到期的卡片！")
            return
        for card in due:
            ans = simpledialog.askstring("複習", f"題目 ({card.answer_field})：{card.prompt_text}\n請輸入答案（或直接確定查看）：")
            if ans is None:
                break
            res = self.review_svc.check_answer(card.card_id, ans)
            hint = "符合 ✓" if res.is_correct else "不符合 ✗（建議選 1）"
            rating = simpledialog.askinteger(
                "FSRS 評分",
                f"參考答案：{card.expected_answer}\n比對結果：{hint}\n\n請輸入評分 (1 忘記 / 2 困難 / 3 記得 / 4 簡單)：",
                minvalue=1,
                maxvalue=4,
            )
            if rating is None:
                break
            self.review_svc.submit_review(card.card_id, rating, user_answer=ans, is_correct=res.is_correct)
        messagebox.showinfo("複習結束", "本輪複習已完成！")

    def _on_import_csv(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if path:
            rep = self.csv_svc.import_notes(path)
            self._refresh_notes()
            messagebox.showinfo("匯入結果", f"新增筆記 {rep.created_notes}、卡片 {rep.created_cards}、重複略過 {rep.skipped_duplicates}")

    def _on_export_csv(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if path:
            cnt = self.csv_svc.export_notes(path)
            messagebox.showinfo("匯出完成", f"已匯出 {cnt} 筆筆記")


def run_gui(db_path: str | Path = DEFAULT_DB_PATH) -> None:
    app = VocabApp(db_path=db_path)
    app.mainloop()
```

- [ ] **Step 2: 驗證 GUI 模組可正確匯入（無語法與匯入錯誤）**

Run: `.\.venv\Scripts\python.exe -c "from src.gui.app import VocabApp, run_gui; print('GUI OK')"`
Expected: `GUI OK`

- [ ] **Step 3: Commit**

```bash
git add src/gui/app.py
git commit -m "feat(gui): implement Tkinter desktop UI for notes, preview, and FSRS review"
```

---

### Task 11: 串接 `main.py`、建立 `data/seed_data.csv` 與全套測試

**Files:**
- Modify: `main.py:1-15`
- Create: `data/seed_data.csv`

**Interfaces:**
- Consumes: `run_cli` from `src.cli.app`; `run_gui` from `src.gui.app`

- [ ] **Step 1: 更新 `main.py`**

```python
"""單字筆記與複習系統 - 程式進入點 (Entry Point)。"""

import sys

from src.cli.app import run_cli
from src.gui.app import run_gui


def main() -> None:
    """根據命令列參數啟動 CLI 或 GUI 介面。"""
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        raise SystemExit(run_cli(sys.argv[2:]))
    run_gui()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 建立範例資料 `data/seed_data.csv`**

```csv
word,meaning,reading,source,example,markdown_body,deck
勉強,學習、用功,べんきょう,日文課 第3課,毎日日本語を勉強します。,## 用法筆記\n可接「する」作為サ變動詞使用。,日文基礎
図書館,圖書館,としょかん,日文課 第4課,図書館で本を読みます。,## 記憶點\n「書」長音為 しょ。,日文基礎
ubiquitous,無所不在的,/juːˈbɪk.wɪ.təs/,TOEFL 單字,Smartphones have become ubiquitous.,## 詞源\n來自拉丁文 *ubique*（到處）。,英文核心
```

- [ ] **Step 3: 執行完整測試套件與 CLI 冒煙測試**

Run: `.\.venv\Scripts\pytest.exe -v`
Expected: 所有測試通過（`test_db.py`, `test_answer_matcher.py`, `test_note_service.py`, `test_deck_card_service.py`, `test_review_service.py`, `test_markdown_service.py`, `test_csv_service.py`, `test_cli.py`）。

- [ ] **Step 4: Commit**

```bash
git add main.py data/seed_data.csv
git commit -m "feat: wire main.py entrypoint and add sample seed_data.csv"
```
