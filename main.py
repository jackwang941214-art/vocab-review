"""單字筆記與複習系統 - 程式進入點 (Entry Point)。"""

import sys


def main() -> None:
    """根據命令列參數啟動 CLI 或 GUI 介面。"""
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        print("啟動 CLI 模式（待實作 src.cli）...")
    else:
        print("啟動 GUI 模式（待實作 src.gui，或加上 --cli 啟動命令列模式）...")


if __name__ == "__main__":
    main()
